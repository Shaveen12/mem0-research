#!/usr/bin/env python3
"""
Simple test script to verify the customer support agent functionality.
This script tests the core features of the mem0-integrated customer support agent.
"""

import os
import sys
import logging
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.customer_support_agent import CustomerSupportAgent
from src.memory.mem0_client import Mem0Client
from src.memory.knowledge_loader import initialize_knowledge_base

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables before running the test.")
        return False
    
    logger.info("✅ Environment variables check passed")
    return True

def test_mem0_client():
    """Test the Mem0 client functionality."""
    logger.info("🧠 Testing Mem0 client...")
    
    try:
        # Initialize client
        client = Mem0Client()
        
        # Test adding a customer interaction
        test_customer_id = "test_customer_001"
        test_interaction = "I'm having trouble with my CloudSync Pro account"
        
        result = client.add_customer_interaction(
            customer_id=test_customer_id,
            interaction=test_interaction,
            metadata={"test": True, "timestamp": datetime.now().isoformat()}
        )
        
        logger.info("✅ Successfully added test interaction to memory")
        
        # Test searching memories
        search_results = client.search_customer_history(
            customer_id=test_customer_id,
            query="CloudSync trouble",
            limit=3
        )
        
        logger.info(f"✅ Found {len(search_results)} relevant memories")
        
        # Clean up test data
        client.delete_customer_memories(test_customer_id)
        logger.info("✅ Cleaned up test data")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Mem0 client test failed: {str(e)}")
        return False

def test_knowledge_base():
    """Test the knowledge base loading functionality."""
    logger.info("📚 Testing knowledge base loader...")
    
    try:
        # Initialize client and knowledge loader
        client = Mem0Client()
        knowledge_loader = initialize_knowledge_base(client)
        
        # Test searching knowledge base
        search_results = knowledge_loader.search_knowledge_base("CloudSync Pro features", limit=3)
        logger.info(f"✅ Found {len(search_results)} knowledge base items")
        
        # Get all knowledge base items
        all_items = knowledge_loader.get_all_knowledge_base_items()
        logger.info(f"✅ Knowledge base contains {len(all_items)} total items")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Knowledge base test failed: {str(e)}")
        return False

def test_customer_support_agent():
    """Test the customer support agent functionality."""
    logger.info("🤖 Testing customer support agent...")
    
    try:
        # Initialize agent
        agent = CustomerSupportAgent(company_name="TechCorp")
        
        # Test customer queries
        test_queries = [
            {
                "customer_id": "test_customer_002",
                "customer_name": "Alice Johnson",
                "query": "Hello, I need help with my CloudSync Pro account"
            },
            {
                "customer_id": "test_customer_002", 
                "customer_name": "Alice Johnson",
                "query": "How much storage do I get?"
            },
            {
                "customer_id": "test_customer_002",
                "customer_name": "Alice Johnson", 
                "query": "Can you remind me what I asked about earlier?"
            }
        ]
        
        for i, test_query in enumerate(test_queries, 1):
            logger.info(f"Testing query {i}: {test_query['query']}")
            
            response_data = agent.handle_customer_query(
                customer_id=test_query["customer_id"],
                query=test_query["query"],
                customer_name=test_query["customer_name"]
            )
            
            logger.info(f"✅ Response generated (length: {len(response_data['response'])} chars)")
            logger.info(f"   Context used: {response_data['context_used']}")
            logger.info(f"   Context items: {response_data['context_items_count']}")
            
            # Show a snippet of the response
            response_snippet = response_data['response'][:100] + "..." if len(response_data['response']) > 100 else response_data['response']
            logger.info(f"   Response: {response_snippet}")
            
        # Test getting customer history
        history = agent.get_customer_history("test_customer_002")
        logger.info(f"✅ Retrieved {len(history)} items from customer history")
        
        # Clean up test data
        agent.clear_customer_history("test_customer_002")
        logger.info("✅ Cleaned up test customer data")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Customer support agent test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    logger.info("🚀 Starting TechCorp Customer Support Agent Tests")
    logger.info("=" * 60)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Mem0 Client", test_mem0_client),
        ("Knowledge Base", test_knowledge_base),
        ("Customer Support Agent", test_customer_support_agent)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name} test...")
        logger.info("-" * 40)
        
        if test_func():
            passed_tests += 1
            logger.info(f"✅ {test_name} test PASSED")
        else:
            logger.error(f"❌ {test_name} test FAILED")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        logger.info("🎉 All tests passed! The customer support agent is ready to use.")
        logger.info("\nTo run the Streamlit UI:")
        logger.info("  streamlit run src/ui/streamlit_app.py")
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 