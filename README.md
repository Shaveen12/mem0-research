# TechCorp Customer Support Agent with Mem0

A demonstration project showcasing how to integrate **Mem0** (memory layer for AI) with **LangChain** and **OpenAI** to build a contextual customer support agent. This project demonstrates the core features of Mem0 for persistent memory in AI applications.

![Customer Support Agent](https://img.shields.io/badge/Powered%20by-Mem0%20%2B%20LangChain%20%2B%20OpenAI-blue)

## 🌟 Features

- **Contextual Memory**: Remembers customer interactions and preferences using Mem0
- **Knowledge Base Integration**: Pre-loaded company information, FAQs, and troubleshooting guides
- **Interactive UI**: Beautiful Streamlit interface for testing and demonstration
- **Memory Visualization**: See how memories are stored and retrieved in real-time
- **Customer History**: Track and manage individual customer interaction histories
- **Semantic Search**: Find relevant information from past interactions and knowledge base

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│ Support Agent   │────│   Mem0 Client   │
│                 │    │   (LangChain)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   OpenAI API    │    │ Vector Database │
                       │                 │    │   (ChromaDB)    │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- (Optional) Mem0 API key for cloud features

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mem0-research
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
export OPENAI_API_KEY="your_openai_api_key_here"

# Optional (for Mem0 cloud features)
export MEM0_API_KEY="your_mem0_api_key_here"
```

You can also copy the example file:
```bash
cp env_example.txt .env
# Edit .env with your actual API keys
```

### 4. Test the Installation

Run the test script to verify everything is working:

```bash
python test_agent.py
```

### 5. Launch the Streamlit UI

```bash
streamlit run src/ui/streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`.

## 📖 Usage Guide

### Basic Usage

1. **Start a Conversation**: Type a message in the chat interface
2. **Customer Context**: Change customer ID to simulate different customers
3. **Memory Visualization**: Watch how memories are stored and retrieved in the sidebar
4. **Knowledge Search**: Use the knowledge base search to find company information

### Example Conversations

Try these sample conversations to see Mem0 in action:

**Customer 1 (customer_001):**
```
User: Hi, I'm having trouble with CloudSync Pro
Agent: [Responds with help and stores the interaction]

User: What are the pricing plans?
Agent: [Provides pricing info and remembers the context]

User: Can you remind me what I asked about earlier?
Agent: [Recalls the CloudSync Pro issue using memory]
```

**Customer 2 (customer_002):**
```
User: I prefer email communication over phone calls
Agent: [Stores this preference]

User: I need help with DataAnalytics Suite
Agent: [Provides help while remembering the communication preference]
```

### Key Features to Explore

1. **Memory Persistence**: Switch between customers and see how memories are isolated
2. **Context Retrieval**: Ask follow-up questions and see how previous context is used
3. **Knowledge Integration**: Ask about products, policies, or troubleshooting
4. **Memory Management**: Clear customer memories or reload the knowledge base

## 🧠 Understanding Mem0 Integration

### How Memory Works

1. **Storage**: Every customer interaction is stored with metadata
2. **Retrieval**: Relevant memories are searched based on semantic similarity
3. **Context**: Retrieved memories provide context for generating responses
4. **Isolation**: Each customer has their own memory space

### Memory Types

- **Customer Interactions**: Questions, issues, and responses
- **Customer Preferences**: Communication preferences, product interests
- **Knowledge Base**: Company information, FAQs, troubleshooting guides

### Memory Metadata

Each memory includes:
- Customer ID
- Timestamp
- Interaction type
- Customer name
- Additional context

## 🏢 TechCorp (Fictional Company)

The demo uses a fictional company "TechCorp" with these products:

### Products
- **CloudSync Pro**: Enterprise cloud storage solution
- **DataAnalytics Suite**: Business intelligence platform  
- **SecureVPN**: High-speed VPN service

### Knowledge Base Includes
- Company information and contact details
- Product features and pricing
- FAQs for common questions
- Troubleshooting guides
- Company policies (Privacy, Terms, Refunds)

## 🔧 Project Structure

```
mem0-research/
├── src/
│   ├── agents/
│   │   └── customer_support_agent.py    # Main agent logic
│   ├── memory/
│   │   ├── mem0_client.py               # Mem0 integration wrapper
│   │   └── knowledge_loader.py          # Knowledge base management
│   └── ui/
│       └── streamlit_app.py             # Streamlit interface
├── data/
│   └── sample_knowledge_base.py         # TechCorp company data
├── test_agent.py                        # Test script
├── requirements.txt                     # Python dependencies
└── README.md                           # This file
```

## 🧪 Testing

The project includes comprehensive tests:

```bash
python test_agent.py
```

Tests cover:
- Mem0 client functionality
- Knowledge base loading
- Customer support agent responses
- Memory storage and retrieval

## 🎯 Core Mem0 Features Demonstrated

### 1. Memory Storage
```python
# Store customer interactions
agent.handle_customer_query(
    customer_id="customer_001",
    query="I need help with CloudSync",
    customer_name="John Doe"
)
```

### 2. Memory Retrieval
```python
# Search relevant memories
memories = client.search_customer_history(
    customer_id="customer_001",
    query="CloudSync issue",
    limit=5
)
```

### 3. Context Integration
```python
# Use memories to provide context
context = self._get_customer_context(customer_id, query)
response = llm.invoke(prompt_with_context)
```

### 4. Memory Management
```python
# Clear customer memories
agent.clear_customer_history("customer_001")

# Add preferences
agent.add_customer_preference(
    customer_id="customer_001",
    preference="Prefers email communication",
    category="communication"
)
```

## 🔍 Key Benefits of Mem0 Integration

1. **Persistent Context**: Conversations continue naturally across sessions
2. **Personalization**: Responses adapt based on customer history and preferences
3. **Efficiency**: Agents don't need to re-ask for information
4. **Scalability**: Each customer has isolated memory space
5. **Semantic Search**: Find relevant information using natural language queries

## 🛠️ Customization

### Adding New Knowledge
Edit `data/sample_knowledge_base.py` to add:
- New products
- Additional FAQs
- Company policies
- Troubleshooting guides

### Modifying the Agent
Edit `src/agents/customer_support_agent.py` to:
- Change the system prompt
- Add new capabilities
- Modify response formatting

### UI Customization
Edit `src/ui/streamlit_app.py` to:
- Change the interface layout
- Add new features
- Modify styling

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for LLM functionality |
| `MEM0_API_KEY` | No | Mem0 API key for cloud features |

## 🤝 Contributing

This is a demonstration project. Feel free to:
- Fork and experiment
- Add new features
- Improve the UI
- Extend the knowledge base

## 📄 License

This project is for educational and demonstration purposes.

## 🆘 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `OPENAI_API_KEY` is set correctly
2. **Import Errors**: Make sure all dependencies are installed
3. **Memory Issues**: Check that Mem0 client initializes properly
4. **UI Not Loading**: Verify Streamlit is installed and run from project root

### Getting Help

1. Check the test script output: `python test_agent.py`
2. Review the Streamlit logs in the terminal
3. Ensure all requirements are installed: `pip install -r requirements.txt`

## 🎉 What's Next?

After exploring this demo, you can:

1. **Integrate with Real Systems**: Connect to actual customer databases
2. **Add More Memory Types**: Store product usage, purchase history
3. **Enhance UI**: Build a production-ready interface
4. **Scale Up**: Deploy with proper vector databases and cloud infrastructure
5. **Add Analytics**: Track memory usage and agent performance

---

**Happy exploring with Mem0! 🚀** 