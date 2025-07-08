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
    
    def __init__(self, company_name: str = "TechCorp", mem0_config: Optional[Dict] = None):
        """
        Initialize the customer support agent.
        
        Args:
            company_name: Name of the company for context
            mem0_config: Optional configuration for Mem0 client
        """
        self.company_name = company_name
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=2000
        )
        
        # Initialize Mem0 client
        self.memory_client = Mem0Client(mem0_config)
        
        # Define the system prompt template
        self.system_prompt = f"""You are a helpful and empathetic customer support agent for {company_name}. 

Your role is to:
1. Assist customers with their questions and issues
2. Provide accurate and helpful information
3. Maintain a professional yet friendly tone
4. Use past interaction context to personalize responses
5. Escalate complex issues when appropriate
6. Remember customer preferences and history

Guidelines:
- Always greet customers warmly
- Listen actively to their concerns
- Provide clear, step-by-step solutions when possible
- Ask clarifying questions if needed
- Show empathy for customer frustrations
- End conversations positively

Use the provided context from previous interactions to give personalized responses.
If you don't have specific information, be honest about limitations and offer to help find the answer.
"""
        
        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.system_prompt),
            MessagesPlaceholder(variable_name="context"),
            HumanMessage(content="{input}")
        ])
        
        self.logger.info(f"Customer support agent initialized for {company_name}")
    
    def _get_customer_context(self, customer_id: str, query: str, limit: int = 3) -> List[Dict]:
        """
        Retrieve relevant context from customer's interaction history.
        
        Args:
            customer_id: Unique identifier for the customer
            query: Current customer query
            limit: Maximum number of context items to retrieve
            
        Returns:
            List of relevant context items
        """
        try:
            # Search for relevant memories
            relevant_memories = self.memory_client.search_customer_history(
                customer_id=customer_id,
                query=query,
                limit=limit
            )
            
            return relevant_memories
            
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
            return "No previous interaction history available."
        
        formatted_context = "Previous interaction context:\n"
        for i, item in enumerate(context_items, 1):
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
            
            # Prepare the prompt
            prompt_input = {
                "context": [SystemMessage(content=formatted_context)],
                "input": query
            }
            
            # Generate response using LangChain
            messages = self.prompt_template.format_messages(**prompt_input)
            response = self.llm.invoke(messages)
            
            response_text = response.content
            
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