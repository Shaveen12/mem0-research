import os
from typing import List, Dict, Any, Optional
from mem0 import Memory
import logging

class Mem0Client:
    """
    A wrapper class for Mem0 memory operations specifically designed for customer support agents.
    Provides simplified methods for storing and retrieving customer interactions and context.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Mem0 client with configuration.
        
        Args:
            config: Optional configuration dictionary. If None, uses default config.
        """
        self.logger = logging.getLogger(__name__)
        
        # Default configuration optimized for customer support
        default_config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.1,
                    "max_tokens": 2000,
                },
            }
        }
        
        # Use provided config or default
        self.config = config or default_config
        
        try:
            self.memory = Memory.from_config(self.config)
            self.logger.info("Mem0 client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Mem0 client: {e}")
            raise
    
    def add_customer_interaction(
        self, 
        customer_id: str, 
        interaction: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a customer interaction to memory.
        
        Args:
            customer_id: Unique identifier for the customer
            interaction: The interaction text (question, issue, etc.)
            metadata: Additional metadata about the interaction
            
        Returns:
            Result of the memory addition operation
        """
        try:
            # Prepare metadata
            interaction_metadata = {
                "type": "customer_interaction",
                "timestamp": metadata.get("timestamp") if metadata else None,
                **(metadata or {})
            }
            
            result = self.memory.add(
                interaction, 
                user_id=customer_id, 
                metadata=interaction_metadata
            )
            
            self.logger.info(f"Added interaction for customer {customer_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to add interaction for customer {customer_id}: {e}")
            raise
    
    def add_conversation(
        self, 
        customer_id: str, 
        messages: List[Dict[str, str]], 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a full conversation to memory.
        
        Args:
            customer_id: Unique identifier for the customer
            messages: List of message dictionaries with 'role' and 'content' keys
            metadata: Additional metadata about the conversation
            
        Returns:
            Result of the memory addition operation
        """
        try:
            # Prepare metadata
            conversation_metadata = {
                "type": "conversation",
                "message_count": len(messages),
                **(metadata or {})
            }
            
            result = self.memory.add(
                messages, 
                user_id=customer_id, 
                metadata=conversation_metadata
            )
            
            self.logger.info(f"Added conversation for customer {customer_id} ({len(messages)} messages)")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to add conversation for customer {customer_id}: {e}")
            raise
    
    def search_customer_history(
        self, 
        customer_id: str, 
        query: str, 
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant memories for a specific customer.
        
        Args:
            customer_id: Unique identifier for the customer
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of relevant memories
        """
        try:
            results = self.memory.search(
                query=query,
                user_id=customer_id,
                limit=limit
            )
            
            self.logger.info(f"Found {len(results)} relevant memories for customer {customer_id}")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to search memories for customer {customer_id}: {e}")
            raise
    
    def get_all_customer_memories(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Get all memories for a specific customer.
        
        Args:
            customer_id: Unique identifier for the customer
            
        Returns:
            List of all memories for the customer
        """
        try:
            result = self.memory.get_all(user_id=customer_id)
            memories = result.get('results', []) if isinstance(result, dict) else result
            
            self.logger.info(f"Retrieved {len(memories)} memories for customer {customer_id}")
            return memories
            
        except Exception as e:
            self.logger.error(f"Failed to get all memories for customer {customer_id}: {e}")
            raise
    
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
            category: Category of the preference (e.g., 'product', 'communication', 'general')
            
        Returns:
            Result of the memory addition operation
        """
        try:
            metadata = {
                "type": "preference",
                "category": category
            }
            
            result = self.memory.add(
                preference, 
                user_id=customer_id, 
                metadata=metadata
            )
            
            self.logger.info(f"Added preference for customer {customer_id} in category {category}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to add preference for customer {customer_id}: {e}")
            raise
    
    def delete_customer_memories(self, customer_id: str) -> Dict[str, Any]:
        """
        Delete all memories for a specific customer.
        
        Args:
            customer_id: Unique identifier for the customer
            
        Returns:
            Result of the deletion operation
        """
        try:
            result = self.memory.delete_all(user_id=customer_id)
            
            self.logger.info(f"Deleted all memories for customer {customer_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to delete memories for customer {customer_id}: {e}")
            raise 