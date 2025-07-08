import streamlit as st
import os
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Custom CSS for better styling and improved contrast
st.markdown("""
<style>
    /* Main theme improvements */
    .main-header {
        color: #1a365d;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1a365d;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    /* Chat message styling with better contrast */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-size: 14px;
        line-height: 1.5;
    }
    
    .user-message {
        background-color: #f0f8ff;
        border-left: 4px solid #1e40af;
        color: #1e3a8a;
    }
    
    .user-message strong {
        color: #1e40af;
    }
    
    .assistant-message {
        background-color: #faf5ff;
        border-left: 4px solid #7c3aed;
        color: #5b21b6;
    }
    
    .assistant-message strong {
        color: #7c3aed;
    }
    
    /* Memory and knowledge items with better readability */
    .memory-item {
        background-color: #fffbeb;
        border: 2px solid #d97706;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        color: #92400e;
        font-size: 13px;
        line-height: 1.4;
    }
    
    .memory-item strong {
        color: #b45309;
    }
    
    .knowledge-item {
        background-color: #f0fdf4;
        border: 2px solid #16a34a;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        color: #15803d;
        font-size: 13px;
        line-height: 1.4;
    }
    
    .knowledge-item strong {
        color: #166534;
    }
    
    /* Error and success messages with high contrast */
    .error-message {
        background-color: #fef2f2;
        border: 2px solid #dc2626;
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .success-message {
        background-color: #f0fdf4;
        border: 2px solid #16a34a;
        color: #166534;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Improve sidebar text contrast */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Improve input field contrast */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #d1d5db;
        color: #1f2937;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Improve button contrast */
    .stButton > button {
        background-color: #3b82f6;
        color: #ffffff;
        border: none;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
    }
    
    /* Improve metric display */
    .css-1r6slb0 {
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Improve expander contrast */
    .streamlit-expanderHeader {
        background-color: #f1f5f9;
        color: #1e293b;
        font-weight: 500;
    }
    
    /* Improve chat input */
    .stChatInput > div > div > div > div {
        background-color: #ffffff;
        border: 2px solid #d1d5db;
    }
    
    .stChatInput > div > div > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Improve general text readability */
    .stMarkdown {
        color: #1f2937;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1e293b;
    }
    
    /* Improve sidebar headers */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #1e293b;
    }
    
    /* Improve divider visibility */
    .css-1wbqy5l {
        border-color: #d1d5db;
    }
    
    /* Improve spinner contrast */
    .stSpinner > div {
        border-top-color: #3b82f6;
    }
    
    /* Improve help text */
    .stTextInput > label > div > p {
        color: #6b7280;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agent():
    """Initialize the customer support agent with caching."""
    try:
        # Initialize memory client first
        from src.memory.mem0_client import Mem0Client
        memory_client = Mem0Client()
        
        # Initialize knowledge base
        knowledge_loader = initialize_knowledge_base(memory_client)
        
        # Initialize the agent with knowledge loader
        agent = CustomerSupportAgent(company_name="TechCorp", knowledge_loader=knowledge_loader)
        
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