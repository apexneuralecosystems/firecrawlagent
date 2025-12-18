# Agentic RAG Workflow Implementation

This codebase has been enhanced with an **Agentic AI architecture** that uses specialized agents for different tasks.

## 🎯 Agentic Architecture Overview

The system now uses multiple specialized agents that work together to process queries:

### 🤖 Agents

1. **RetrievalAgent** - Specialized in document retrieval from vector stores
2. **RelevanceAgent** - Evaluates relevance of retrieved documents
3. **WebSearchAgent** - Performs web searches using FireCrawl API
4. **QueryAgent** - Generates final answers based on context
5. **OrchestratorAgent** - Coordinates all agents and manages workflow

### 🔄 Workflow Process

```
User Query
    ↓
OrchestratorAgent
    ↓
┌─────────────────┐
│ RetrievalAgent  │ → Retrieves relevant documents
└─────────────────┘
    ↓
┌─────────────────┐
│ RelevanceAgent  │ → Evaluates document relevance
└─────────────────┘
    ↓
┌─────────────────┐
│ WebSearchAgent  │ → Searches web if needed (conditional)
└─────────────────┘
    ↓
┌─────────────────┐
│ QueryAgent      │ → Generates final answer
└─────────────────┘
    ↓
Final Response
```

## 🚀 Key Features

### 1. **Modular Agent Design**
- Each agent has a specific responsibility
- Agents can be easily extended or replaced
- Clear separation of concerns

### 2. **Intelligent Orchestration**
- OrchestratorAgent decides when to use each agent
- Conditional web search based on relevance evaluation
- Context passing between agents

### 3. **Memory & State Management**
- Each agent maintains its own memory
- Context is passed through the workflow
- State is preserved across agent interactions

### 4. **Error Handling**
- Each agent handles errors independently
- Graceful degradation if an agent fails
- Detailed error reporting

## 📁 File Structure

```
firecrawlagnet/
├── agentic_workflow.py    # New agentic implementation
├── workflow.py            # Original workflow (still available)
├── app.py                 # Updated to use agentic workflow
└── ...
```

## 🔧 Usage

The agentic workflow is automatically used when you run the app:

```bash
python -m streamlit run app.py
```

### Switching Between Workflows

To switch back to the original workflow, edit `app.py`:

```python
# Use original workflow
from workflow import CorrectiveRAGWorkflow
workflow = CorrectiveRAGWorkflow(...)

# Or use agentic workflow (default)
from agentic_workflow import AgenticRAGWorkflow
workflow = AgenticRAGWorkflow(...)
```

## 🎨 Agent Customization

### Adding a New Agent

```python
class CustomAgent(Agent):
    """Your custom agent."""
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        # Your agent logic here
        return {
            "agent": self.name,
            "task": "custom_task",
            "result": "result",
            "status": "success"
        }
```

### Registering with Orchestrator

```python
orchestrator = OrchestratorAgent(
    "Orchestrator",
    llm,
    {
        "retrieval": retrieval_agent,
        "relevance": relevance_agent,
        "web_search": web_search_agent,
        "query": query_agent,
        "custom": custom_agent  # Add your agent
    }
)
```

## 🔍 Benefits of Agentic Architecture

1. **Scalability** - Easy to add new agents for new capabilities
2. **Maintainability** - Each agent is independently testable
3. **Flexibility** - Agents can be swapped or reconfigured
4. **Transparency** - Clear visibility into each step of processing
5. **Extensibility** - Simple to add new tools or capabilities

## 🧪 Testing Agents

You can test individual agents:

```python
from agentic_workflow import RetrievalAgent, RelevanceAgent

# Test retrieval agent
retrieval_agent = RetrievalAgent("TestAgent", llm, retriever)
result = await retrieval_agent.execute("test query")
print(result)
```

## 📊 Monitoring

Each agent returns structured results:

```python
{
    "agent": "AgentName",
    "task": "task_type",
    "result": "actual_result",
    "status": "success|error",
    # Additional agent-specific fields
}
```

## 🔐 Security

- Agents operate with the same security context
- API keys are managed centrally
- No additional security risks compared to original workflow

## 🚧 Future Enhancements

Potential improvements:
- Agent-to-agent communication protocols
- Agent learning and adaptation
- Dynamic agent selection based on query type
- Agent performance metrics and optimization
- Multi-agent collaboration patterns

## 📝 Notes

- The agentic workflow maintains full compatibility with the existing UI
- All existing features (PDF upload, chat, etc.) work the same way
- The agentic approach provides better structure for future enhancements







