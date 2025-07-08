import os
import logging
from typing import Dict, List, Any
from ..memory.mem0_client import Mem0Client
from data.sample_knowledge_base import get_searchable_content

class KnowledgeBaseLoader:
    """
    Loads knowledge base content into Mem0 memory for the customer support agent.
    """
    
    def __init__(self, mem0_client: Mem0Client):
        """
        Initialize the knowledge base loader.
        
        Args:
            mem0_client: Initialized Mem0Client instance
        """
        self.mem0_client = mem0_client
        self.logger = logging.getLogger(__name__)
        self.knowledge_base_user_id = "techcorp_knowledge_base"
    
    def load_knowledge_base(self) -> Dict[str, Any]:
        """
        Load all knowledge base content into memory.
        
        Returns:
            Dictionary with loading results
        """
        try:
            # Get searchable content
            searchable_items = get_searchable_content()
            
            loaded_count = 0
            errors = []
            
            self.logger.info(f"Loading {len(searchable_items)} knowledge base items...")
            
            for item in searchable_items:
                try:
                    # Prepare metadata
                    metadata = {
                        "type": item["type"],
                        "source": "knowledge_base",
                        "loaded_at": "initial_load"
                    }
                    
                    # Add additional metadata based on item type
                    if "category" in item:
                        metadata["category"] = item["category"]
                    if "product" in item:
                        metadata["product"] = item["product"]
                    if "title" in item:
                        metadata["title"] = item["title"]
                    
                    # Add to memory
                    result = self.mem0_client.memory.add(
                        item["content"],
                        user_id=self.knowledge_base_user_id,
                        metadata=metadata
                    )
                    
                    loaded_count += 1
                    
                except Exception as e:
                    error_msg = f"Failed to load item {item.get('type', 'unknown')}: {str(e)}"
                    errors.append(error_msg)
                    self.logger.error(error_msg)
            
            self.logger.info(f"Successfully loaded {loaded_count} knowledge base items")
            
            return {
                "success": True,
                "loaded_count": loaded_count,
                "total_items": len(searchable_items),
                "errors": errors
            }
            
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base: {e}")
            return {
                "success": False,
                "error": str(e),
                "loaded_count": 0,
                "total_items": 0,
                "errors": []
            }
    
    def search_knowledge_base(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for relevant information.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of relevant knowledge base items
        """
        try:
            results = self.mem0_client.memory.search(
                query=query,
                user_id=self.knowledge_base_user_id,
                limit=limit
            )
            
            self.logger.info(f"Found {len(results)} relevant knowledge base items for query: {query}")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to search knowledge base: {e}")
            return []
    
    def get_all_knowledge_base_items(self) -> List[Dict[str, Any]]:
        """
        Get all knowledge base items from memory.
        
        Returns:
            List of all knowledge base items
        """
        try:
            result = self.mem0_client.memory.get_all(user_id=self.knowledge_base_user_id)
            memories = result.get('results', []) if isinstance(result, dict) else result
            
            self.logger.info(f"Retrieved {len(memories)} knowledge base items")
            return memories
            
        except Exception as e:
            self.logger.error(f"Failed to get knowledge base items: {e}")
            return []
    
    def clear_knowledge_base(self) -> Dict[str, Any]:
        """
        Clear all knowledge base items from memory.
        
        Returns:
            Result of the operation
        """
        try:
            result = self.mem0_client.memory.delete_all(user_id=self.knowledge_base_user_id)
            
            self.logger.info("Cleared knowledge base from memory")
            return {"success": True, "result": result}
            
        except Exception as e:
            self.logger.error(f"Failed to clear knowledge base: {e}")
            return {"success": False, "error": str(e)}
    
    def reload_knowledge_base(self) -> Dict[str, Any]:
        """
        Clear and reload the knowledge base.
        
        Returns:
            Result of the operation
        """
        try:
            # Clear existing knowledge base
            clear_result = self.clear_knowledge_base()
            if not clear_result["success"]:
                return clear_result
            
            # Reload knowledge base
            load_result = self.load_knowledge_base()
            
            self.logger.info("Knowledge base reloaded successfully")
            return load_result
            
        except Exception as e:
            self.logger.error(f"Failed to reload knowledge base: {e}")
            return {"success": False, "error": str(e)}


def initialize_knowledge_base(mem0_client: Mem0Client) -> KnowledgeBaseLoader:
    """
    Initialize and load the knowledge base.
    
    Args:
        mem0_client: Initialized Mem0Client instance
        
    Returns:
        KnowledgeBaseLoader instance
    """
    loader = KnowledgeBaseLoader(mem0_client)
    
    # Check if knowledge base is already loaded
    existing_items = loader.get_all_knowledge_base_items()
    
    if len(existing_items) == 0:
        # Load knowledge base for the first time
        result = loader.load_knowledge_base()
        if result["success"]:
            logging.info(f"Knowledge base initialized with {result['loaded_count']} items")
        else:
            logging.error(f"Failed to initialize knowledge base: {result.get('error', 'Unknown error')}")
    else:
        logging.info(f"Knowledge base already exists with {len(existing_items)} items")
    
    return loader 