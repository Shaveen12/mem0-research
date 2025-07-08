import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from ..memory.mem0_client import Mem0Client


class CustomerSupportAgent:
    """
    A customer support agent that combines LangChain, OpenAI, and Mem0 for 
    contextual and personalized customer support interactions.
    """
    
    def __init__(self, company_name: str = "TechCorp", mem0_config: Optional[Dict] = None, knowledge_loader=None):
        """
        Initialize the customer support agent.
        
        Args:
            company_name: Name of the company for context
            mem0_config: Optional configuration for Mem0 client
            knowledge_loader: KnowledgeBaseLoader instance for accessing company knowledge
        """
        self.company_name = company_name
        self.knowledge_loader = knowledge_loader
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_completion_tokens=2000
        )
        
        # Initialize Mem0 client
        self.memory_client = Mem0Client(mem0_config)
        
        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", f"""You are a helpful customer support agent for {company_name}. 
            
Your role is to:
- Provide accurate, helpful responses to customer queries
- Use the provided context from previous interactions and company knowledge base
- Be professional, empathetic, and solution-oriented
- If you don't know something, admit it and offer to escalate or find more information
- Personalize responses using customer information when available

Context will include:
1. Previous customer interactions and preferences
2. Relevant company knowledge base information (products, FAQs, policies, troubleshooting)

Always prioritize accuracy and helpfulness in your responses."""),
            
            ("human", "Context: {context}"),
            ("human", "Customer Query: {input}"),
            ("human", "Please provide a helpful response based on the context and your knowledge of {company_name}.")
        ])
        
        self.logger.info(f"Customer support agent initialized for {company_name}")
    
    def _get_customer_context(self, customer_id: str, query: str, limit: int = 3) -> List[Dict]:
        """
        Retrieve relevant context from both customer's interaction history and knowledge base.
        
        Args:
            customer_id: Unique identifier for the customer
            query: Current customer query
            limit: Maximum number of context items to retrieve from each source
            
        Returns:
            List of relevant context items
        """
        try:
            all_context = []
            
            # 1. Search customer's personal memory
            customer_memories = self.memory_client.search_customer_history(
                customer_id=customer_id,
                query=query,
                limit=limit
            )
            
            # Add customer memories to context
            for memory in customer_memories:
                if isinstance(memory, dict):
                    memory_copy = memory.copy()  # Create a copy to avoid modifying original
                    memory_copy['source'] = 'customer_history'
                    all_context.append(memory_copy)
            
            # 2. Search knowledge base if available
            knowledge_items = []
            if self.knowledge_loader:
                knowledge_items = self.knowledge_loader.search_knowledge_base(
                    query=query,
                    limit=limit
                )
                
                # Add knowledge base items to context
                for item in knowledge_items:
                    if isinstance(item, dict):
                        item_copy = item.copy()  # Create a copy to avoid modifying original
                        item_copy['source'] = 'knowledge_base'
                        all_context.append(item_copy)
                    elif isinstance(item, str):
                        # Handle string results by wrapping them in a dict
                        item_dict = {'memory': item, 'source': 'knowledge_base'}
                        all_context.append(item_dict)
            
            self.logger.info(f"Retrieved {len(customer_memories)} customer memories and {len(knowledge_items)} knowledge base items")
            return all_context
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve context for customer {customer_id}: {e}")
            return []
    
    def _format_context(self, context_items: List[Dict]) -> str:
        """
        Format context items into a readable string for the prompt.
        
        Args:
            context_items: List of context dictionaries
            
        Returns:
            Formatted context string
        """
        if not context_items:
            return "No previous interaction history or relevant knowledge base information available."
        
        formatted_context = ""
        
        # Separate customer history and knowledge base items
        customer_items = [item for item in context_items if item.get('source') == 'customer_history']
        knowledge_items = [item for item in context_items if item.get('source') == 'knowledge_base']
        
        # Format customer history
        if customer_items:
            formatted_context += "Previous Customer Interactions:\n"
            for i, item in enumerate(customer_items, 1):
                memory_text = item.get('memory', 'No memory text available')
                formatted_context += f"{i}. {memory_text}\n"
            formatted_context += "\n"
        
        # Format knowledge base information
        if knowledge_items:
            formatted_context += "Relevant Company Knowledge:\n"
            for i, item in enumerate(knowledge_items, 1):
                memory_text = item.get('memory', 'No memory text available')
                formatted_context += f"{i}. {memory_text}\n"
        
        return formatted_context
    
    def handle_customer_query(
        self, 
        customer_id: str, 
        query: str, 
        customer_name: Optional[str] = None,
        save_interaction: bool = True
    ) -> Dict[str, Any]:
        """
        Handle a customer query with context from memory.
        
        Args:
            customer_id: Unique identifier for the customer
            query: Customer's query or issue
            customer_name: Optional customer name for personalization
            save_interaction: Whether to save this interaction to memory
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            # Get relevant context from memory
            context_items = self._get_customer_context(customer_id, query)
            formatted_context = self._format_context(context_items)
            
            # Add customer name context if provided
            if customer_name:
                formatted_context += f"\nCustomer Information:\n- Customer Name: {customer_name}\n- Customer ID: {customer_id}"
            
            # Prepare the prompt
            prompt_input = {
                "context": formatted_context,
                "input": query,
                "company_name": self.company_name
            }
            
            # Generate response using LangChain
            messages = self.prompt_template.format_messages(**prompt_input)
            response = self.llm.invoke(messages)
            
            response_text = str(response.content) if response.content else "I apologize, but I couldn't generate a proper response. Please try again."
            
            # Save the interaction to memory if requested
            if save_interaction:
                self._save_interaction_to_memory(customer_id, query, response_text, customer_name)
            
            # Prepare response metadata
            response_data = {
                "response": response_text,
                "customer_id": customer_id,
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "context_used": len(context_items) > 0,
                "context_items_count": len(context_items)
            }
            
            self.logger.info(f"Handled query for customer {customer_id}")
            return response_data
            
        except Exception as e:
            self.logger.error(f"Failed to handle query for customer {customer_id}: {e}")
            error_response = {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again or contact our technical support team.",
                "customer_id": customer_id,
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "context_used": False,
                "context_items_count": 0
            }
            return error_response
    
    def _save_interaction_to_memory(
        self, 
        customer_id: str, 
        query: str, 
        response: str, 
        customer_name: Optional[str] = None
    ):
        """
        Save the customer interaction to memory.
        
        Args:
            customer_id: Unique identifier for the customer
            query: Customer's query
            response: Agent's response
            customer_name: Optional customer name
        """
        try:
            # Create conversation format
            conversation = [
                {"role": "user", "content": query},
                {"role": "assistant", "content": response}
            ]
            
            # Prepare metadata
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "customer_name": customer_name,
                "interaction_type": "support_chat"
            }
            
            # Save to memory
            self.memory_client.add_conversation(
                customer_id=customer_id,
                messages=conversation,
                metadata=metadata
            )
            
            self.logger.info(f"Saved interaction to memory for customer {customer_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to save interaction to memory for customer {customer_id}: {e}")
    
    def add_customer_preference(
        self, 
        customer_id: str, 
        preference: str, 
        category: str = "general"
    ) -> Dict[str, Any]:
        """
        Add a customer preference to memory.
        
        Args:
            customer_id: Unique identifier for the customer
            preference: The preference text
            category: Category of the preference
            
        Returns:
            Result of the operation
        """
        try:
            result = self.memory_client.add_customer_preference(
                customer_id=customer_id,
                preference=preference,
                category=category
            )
            
            self.logger.info(f"Added preference for customer {customer_id}")
            return {"success": True, "result": result}
            
        except Exception as e:
            self.logger.error(f"Failed to add preference for customer {customer_id}: {e}")
            return {"success": False, "error": str(e)}
    
    def get_customer_history(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Get all interaction history for a customer.
        
        Args:
            customer_id: Unique identifier for the customer
            
        Returns:
            List of customer memories
        """
        try:
            memories = self.memory_client.get_all_customer_memories(customer_id)
            self.logger.info(f"Retrieved {len(memories)} memories for customer {customer_id}")
            return memories
            
        except Exception as e:
            self.logger.error(f"Failed to get history for customer {customer_id}: {e}")
            return []
    
    def clear_customer_history(self, customer_id: str) -> Dict[str, Any]:
        """
        Clear all interaction history for a customer.
        
        Args:
            customer_id: Unique identifier for the customer
            
        Returns:
            Result of the operation
        """
        try:
            result = self.memory_client.delete_customer_memories(customer_id)
            self.logger.info(f"Cleared history for customer {customer_id}")
            return {"success": True, "result": result}
            
        except Exception as e:
            self.logger.error(f"Failed to clear history for customer {customer_id}: {e}")
            return {"success": False, "error": str(e)} 