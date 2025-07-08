import streamlit as st
import os
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import traceback

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents.customer_support_agent import CustomerSupportAgent
from src.memory.mem0_client import Mem0Client
from src.memory.knowledge_loader import initialize_knowledge_base
from data.sample_knowledge_base import get_knowledge_base_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="TechCorp Customer Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        color: #2E86AB;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #2E86AB;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #F3E5F5;
        border-left: 4px solid #9C27B0;
    }
    .memory-item {
        background-color: #FFF3E0;
        border: 1px solid #FF9800;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    .knowledge-item {
        background-color: #E8F5E8;
        border: 1px solid #4CAF50;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    .error-message {
        background-color: #FFEBEE;
        border: 1px solid #F44336;
        color: #D32F2F;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #E8F5E8;
        border: 1px solid #4CAF50;
        color: #2E7D32;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agent():
    """Initialize the customer support agent with caching."""
    try:
        # Initialize the agent
        agent = CustomerSupportAgent(company_name="TechCorp")
        
        # Initialize knowledge base
        knowledge_loader = initialize_knowledge_base(agent.memory_client)
        
        return agent, knowledge_loader
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        logger.error(f"Agent initialization error: {traceback.format_exc()}")
        return None, None

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "customer_id" not in st.session_state:
        st.session_state.customer_id = "customer_001"
    if "customer_name" not in st.session_state:
        st.session_state.customer_name = "John Doe"
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

def display_chat_message(message: Dict[str, str], is_user: bool = True):
    """Display a chat message with proper styling."""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 {st.session_state.customer_name}:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 TechCorp Support Agent:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)

def display_memory_items(memories: List[Dict], title: str, css_class: str):
    """Display memory items in a formatted way."""
    if memories:
        st.markdown(f"**{title}** ({len(memories)} items)")
        for i, memory in enumerate(memories, 1):
            memory_text = memory.get('memory', 'No memory text')
            metadata = memory.get('metadata', {})
            
            st.markdown(f"""
            <div class="{css_class}">
                <strong>#{i}:</strong> {memory_text}<br>
                <small><em>Type: {metadata.get('type', 'Unknown')}</em></small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"**{title}**: No items found")

def main():
    """Main application function."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 TechCorp Customer Support Agent</h1>', unsafe_allow_html=True)
    st.markdown("*Powered by LangChain, OpenAI, and Mem0 for contextual customer support*")
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ Please set your OPENAI_API_KEY environment variable")
        st.stop()
    
    # Initialize agent
    agent, knowledge_loader = initialize_agent()
    if not agent:
        st.error("Failed to initialize the support agent. Please check your configuration.")
        st.stop()
    
    # Sidebar for customer information and controls
    with st.sidebar:
        st.header("👤 Customer Information")
        
        # Customer details
        new_customer_id = st.text_input(
            "Customer ID", 
            value=st.session_state.customer_id,
            help="Unique identifier for the customer"
        )
        
        new_customer_name = st.text_input(
            "Customer Name", 
            value=st.session_state.customer_name,
            help="Customer's display name"
        )
        
        # Update session state if changed
        if new_customer_id != st.session_state.customer_id:
            st.session_state.customer_id = new_customer_id
            st.session_state.messages = []  # Clear messages when customer changes
            st.rerun()
        
        if new_customer_name != st.session_state.customer_name:
            st.session_state.customer_name = new_customer_name
        
        st.divider()
        
        # Controls
        st.header("🔧 Controls")
        
        if st.button("🗑️ Clear Chat History", help="Clear the current conversation"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🧠 Clear Customer Memory", help="Clear all stored memories for this customer"):
            try:
                result = agent.clear_customer_history(st.session_state.customer_id)
                if result["success"]:
                    st.success("Customer memory cleared successfully!")
                else:
                    st.error(f"Failed to clear memory: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error clearing memory: {str(e)}")
        
        if st.button("📚 Reload Knowledge Base", help="Reload the company knowledge base"):
            try:
                result = knowledge_loader.reload_knowledge_base()
                if result["success"]:
                    st.success(f"Knowledge base reloaded! {result['loaded_count']} items loaded.")
                else:
                    st.error(f"Failed to reload knowledge base: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error reloading knowledge base: {str(e)}")
        
        st.divider()
        
        # Display customer memory
        st.header("🧠 Customer Memory")
        try:
            customer_memories = agent.get_customer_history(st.session_state.customer_id)
            display_memory_items(customer_memories, "Stored Memories", "memory-item")
        except Exception as e:
            st.error(f"Error retrieving customer memory: {str(e)}")
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat Interface")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                display_chat_message(message, is_user=message["role"] == "user")
        
        # Chat input
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get response from agent
            with st.spinner("🤖 Thinking..."):
                try:
                    response_data = agent.handle_customer_query(
                        customer_id=st.session_state.customer_id,
                        query=user_input,
                        customer_name=st.session_state.customer_name
                    )
                    
                    # Add assistant response to chat
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response_data["response"]
                    })
                    
                    # Store conversation metadata
                    st.session_state.conversation_history.append({
                        "timestamp": response_data["timestamp"],
                        "context_used": response_data["context_used"],
                        "context_items_count": response_data["context_items_count"]
                    })
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                    logger.error(f"Error handling query: {traceback.format_exc()}")
            
            st.rerun()
    
    with col2:
        st.header("📊 Context & Analytics")
        
        # Display conversation statistics
        if st.session_state.conversation_history:
            total_interactions = len(st.session_state.conversation_history)
            context_used_count = sum(1 for conv in st.session_state.conversation_history if conv["context_used"])
            
            st.metric("Total Interactions", total_interactions)
            st.metric("Context Used", f"{context_used_count}/{total_interactions}")
            
            if context_used_count > 0:
                avg_context_items = sum(conv["context_items_count"] for conv in st.session_state.conversation_history) / total_interactions
                st.metric("Avg Context Items", f"{avg_context_items:.1f}")
        
        st.divider()
        
        # Knowledge base search
        st.subheader("🔍 Knowledge Base Search")
        search_query = st.text_input("Search knowledge base:", placeholder="Enter search terms...")
        
        if search_query:
            try:
                kb_results = knowledge_loader.search_knowledge_base(search_query, limit=3)
                display_memory_items(kb_results, "Knowledge Base Results", "knowledge-item")
            except Exception as e:
                st.error(f"Error searching knowledge base: {str(e)}")
        
        st.divider()
        
        # Company information
        st.subheader("🏢 Company Info")
        try:
            company_data = get_knowledge_base_data()
            company_info = company_data["company_info"]
            
            st.write(f"**{company_info['name']}**")
            st.write(company_info['description'])
            st.write(f"📞 {company_info['contact']['phone']}")
            st.write(f"📧 {company_info['contact']['email']}")
            
            # Product quick info
            st.subheader("🛍️ Products")
            for product in company_data["products"]:
                with st.expander(f"{product['name']} ({product['category']})"):
                    st.write(product['description'])
                    st.write("**Features:**")
                    for feature in product['features']:
                        st.write(f"• {feature}")
                    
        except Exception as e:
            st.error(f"Error loading company information: {str(e)}")
    
    # Footer
    st.divider()
    st.markdown("---")
    st.markdown(
        "*This is a demo application showcasing Mem0 integration with LangChain and OpenAI for contextual customer support.*"
    )

if __name__ == "__main__":
    main() 