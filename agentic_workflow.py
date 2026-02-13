"""
Agentic RAG Workflow using an agent-based architecture.
This implementation uses specialized agents for different tasks.
"""
import os
from typing import Optional, Any, Dict, List
import re
import requests

# IMPORTANT: Import pydantic_config FIRST to patch base classes before they're used
# This must be imported before any llama-index workflow imports
import pydantic_config  # noqa: F401

from pydantic import ConfigDict

from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    step,
    Workflow,
    Context,
)

from llama_index.core import SummaryIndex
from llama_index.core.schema import Document
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.litellm import LiteLLM
from llama_index.core.llms import LLM
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.schema import NodeWithScore
from dotenv import load_dotenv

load_dotenv()


# Define extract_text_from_response BEFORE patching LiteLLM
def extract_text_from_response(response):
    """Extract text from LLM response, converting BaseMessage objects to strings."""
    from llama_index.core.base.llms.types import CompletionResponse
    
    try:
        from langchain_core.messages.base import BaseMessage
        if isinstance(response, BaseMessage):
            text = response.content if hasattr(response, 'content') else str(response)
            return CompletionResponse(text=str(text), raw=response)
    except (ImportError, AttributeError):
        pass
    
    if isinstance(response, CompletionResponse):
        if hasattr(response, 'text'):
            try:
                from langchain_core.messages.base import BaseMessage
                if isinstance(response.text, BaseMessage):
                    text = response.text.content if hasattr(response.text, 'content') else str(response.text)
                    return CompletionResponse(text=str(text), raw=getattr(response, 'raw', response))
            except (ImportError, AttributeError):
                pass
        if isinstance(response.text, str):
            return response
        return CompletionResponse(text=str(response.text), raw=getattr(response, 'raw', response))
    
    if hasattr(response, 'text'):
        text = response.text
        try:
            from langchain_core.messages.base import BaseMessage
            if isinstance(text, BaseMessage):
                text = text.content if hasattr(text, 'content') else str(text)
        except (ImportError, AttributeError):
            pass
        text = str(text) if not isinstance(text, str) else text
        return CompletionResponse(text=text, raw=response)
    
    if hasattr(response, 'content'):
        text = response.content if isinstance(response.content, str) else str(response.content)
        return CompletionResponse(text=text, raw=response)
    
    return CompletionResponse(text=str(response), raw=response)


# Patch LiteLLM at the class level
_original_litellm_acomplete = LiteLLM.acomplete
_original_litellm_complete = LiteLLM.complete

async def _patched_litellm_acomplete(self, prompt, **kwargs):
    """Patched acomplete that converts BaseMessage to CompletionResponse immediately."""
    response = await _original_litellm_acomplete(self, prompt, **kwargs)
    return extract_text_from_response(response)

def _patched_litellm_complete(self, prompt, **kwargs):
    """Patched complete that converts BaseMessage to CompletionResponse immediately."""
    response = _original_litellm_complete(self, prompt, **kwargs)
    return extract_text_from_response(response)

LiteLLM.acomplete = _patched_litellm_acomplete
LiteLLM.complete = _patched_litellm_complete


class Agent:
    """Base Agent class for agentic workflow."""
    
    def __init__(self, name: str, llm: LLM, tools: List = None):
        self.name = name
        self.llm = llm
        self.tools = tools or []
        self.memory = []
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        """Execute a task and return result."""
        raise NotImplementedError


class RetrievalAgent(Agent):
    """Agent specialized in document retrieval."""
    
    def __init__(self, name: str, llm: LLM, retriever: BaseRetriever):
        super().__init__(name, llm)
        self.retriever = retriever
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        """Retrieve relevant documents."""
        query = task
        nodes = self.retriever.retrieve(query)
        return {
            "agent": self.name,
            "task": "retrieval",
            "result": nodes,
            "status": "success"
        }


class RelevanceAgent(Agent):
    """Agent specialized in relevance evaluation."""
    
    RELEVANCY_PROMPT = PromptTemplate(
        template="""As a grader, evaluate the relevance of a document to a question.

Retrieved Document:
-------------------
{context_str}

User Question:
--------------
{query_str}

Evaluation Criteria:
- Consider keywords and topics related to the question.
- Don't be overly stringent; filter out clearly irrelevant retrievals.

Decision:
- Use 'yes' if relevant, 'no' if not.

Provide your binary score ('yes' or 'no'):"""
    )
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        """Evaluate relevance of documents."""
        nodes = context.get("nodes", [])
        query = context.get("query", "")
        
        relevancy_results = []
        for node in nodes:
            prompt = self.RELEVANCY_PROMPT.format(
                context_str=node.text, 
                query_str=query
            )
            try:
                result = await self.llm.acomplete(prompt)
                result = extract_text_from_response(result)
                relevancy = result.text.lower().strip()
                relevancy_results.append(relevancy)
            except Exception:
                result = self.llm.complete(prompt)
                result = extract_text_from_response(result)
                relevancy = result.text.lower().strip()
                relevancy_results.append(relevancy)
        
        # Clean relevancy results
        relevancy_results = [
            re.sub(r"<think>.*?</think>", "", s, flags=re.DOTALL).strip()
            for s in relevancy_results
        ]
        
        relevant_nodes = [
            nodes[i] for i, result in enumerate(relevancy_results)
            if "yes" in result.lower()
        ]
        
        return {
            "agent": self.name,
            "task": "relevance_evaluation",
            "result": relevant_nodes,
            "all_results": relevancy_results,
            "status": "success"
        }


class WebSearchAgent(Agent):
    """Agent specialized in web search using FireCrawl."""
    
    TRANSFORM_PROMPT = PromptTemplate(
        template="""Refine this query for better search results.

Original Query:
-------
{query_str}
-------

Rephrase or enhance this query to improve search performance. 
Ensure it's concise and aligned with the search objective.

Respond with the optimized query only:"""
    )
    
    def __init__(self, name: str, llm: LLM, firecrawl_api_key: str):
        super().__init__(name, llm)
        self.firecrawl_api_key = firecrawl_api_key
    
    def _firecrawl_search(self, query: str, limit: int = 5) -> str:
        """Perform web search using FireCrawl API."""
        url = "https://api.firecrawl.dev/v1/search"
        payload = {
            "query": query,
            "limit": limit,
            "timeout": 60000,
        }
        headers = {
            "Authorization": f"Bearer {self.firecrawl_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("data"):
                search_results = []
                for result in data["data"]:
                    title = result.get("title", "")
                    description = result.get("description", "")
                    url = result.get("url", "")
                    if title or description:
                        result_text = f"Title: {title}\nDescription: {description}\nURL: {url}\n"
                        search_results.append(result_text)
                return "\n---\n".join(search_results)
            return ""
        except Exception as e:
            print(f"FireCrawl search error: {e}")
            return ""
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        """Perform web search."""
        query = context.get("query", task)
        
        # Transform query for better search
        prompt = self.TRANSFORM_PROMPT.format(query_str=query)
        try:
            result = await self.llm.acomplete(prompt)
            result = extract_text_from_response(result)
            transformed_query = result.text
        except Exception:
            result = self.llm.complete(prompt)
            result = extract_text_from_response(result)
            transformed_query = result.text
        
        # Perform search
        search_results = self._firecrawl_search(transformed_query)
        
        return {
            "agent": self.name,
            "task": "web_search",
            "result": search_results,
            "transformed_query": transformed_query,
            "status": "success"
        }


class QueryAgent(Agent):
    """Agent specialized in generating final answers."""
    
    ANSWER_PROMPT = """As a helpful assistant, answer the user's question based on the given context.

Context:
{context_str}

Question:
{query_str}

Generate a comprehensive answer:"""
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        """Generate final answer."""
        relevant_text = context.get("relevant_text", "")
        search_text = context.get("search_text", "")
        query = context.get("query", task)
        
        if not relevant_text.strip() and not search_text.strip():
            return {
                "agent": self.name,
                "task": "answer_generation",
                "result": "No relevant information found in the documents.",
                "status": "success"
            }
        
        context_str = relevant_text + "\n" + search_text
        prompt = self.ANSWER_PROMPT.format(
            context_str=context_str,
            query_str=query
        )
        
        try:
            result = await self.llm.acomplete(prompt)
            result = extract_text_from_response(result)
            answer = result.text
        except Exception as e:
            return {
                "agent": self.name,
                "task": "answer_generation",
                "result": f"Error generating response: {str(e)}",
                "status": "error"
            }
        
        return {
            "agent": self.name,
            "task": "answer_generation",
            "result": answer,
            "status": "success"
        }


class OrchestratorAgent(Agent):
    """Orchestrator agent that coordinates other agents."""
    
    def __init__(self, name: str, llm: LLM, agents: Dict[str, Agent]):
        super().__init__(name, llm)
        self.agents = agents
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        """Orchestrate agent execution."""
        print(f"DEBUG: Orchestrator starting execution for task: {task[:100]}...")
        context = context or {}
        context["query"] = task
        
        try:
            # Step 1: Retrieval
            print("DEBUG: Step 1 - Retrieval")
            retrieval_agent = self.agents.get("retrieval")
            if retrieval_agent:
                retrieval_result = await retrieval_agent.execute(task, context)
                context["nodes"] = retrieval_result.get("result", [])
                print(f"DEBUG: Retrieved {len(context.get('nodes', []))} nodes")
            
            # Step 2: Relevance Evaluation (SKIP for now to avoid timeout)
            print("DEBUG: Step 2 - Skipping relevance evaluation")
            needs_web_search = False
            
            # Get text from retrieved nodes
            if context.get("nodes"):
                context["relevant_text"] = "\n".join([node.text for node in context["nodes"][:3]])  # Limit to top 3
            else:
                context["relevant_text"] = "No relevant documents found."
            
            # Step 3: Web Search (SKIP - likely causing timeout)
            print("DEBUG: Step 3 - Skipping web search")
            
            # Step 4: Generate Answer
            print("DEBUG: Step 4 - Generating answer")
            query_agent = self.agents.get("query")
            if query_agent:
                answer_result = await query_agent.execute(task, context)
                print("DEBUG: Answer generated successfully")
                return answer_result
            
            print("DEBUG: No query agent available")
            return {
                "agent": self.name,
                "task": "orchestration",
                "result": "No query agent available",
                "status": "error"
            }
        except Exception as e:
            print(f"ERROR in Orchestrator: {e}")
            import traceback
            traceback.print_exc()
            return {
                "agent": self.name,
                "task": "orchestration",
                "result": f"Error: {str(e)}",
                "status": "error"
            }


class AgenticRAGWorkflow(Workflow):
    """Agentic RAG Workflow using specialized agents."""
    
    # Pydantic v2 configuration - base Workflow class is already patched, but set explicitly for safety
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def __init__(
        self,
        index,
        firecrawl_api_key: str,
        llm: Optional[LLM] = None,
        **kwargs: Any
    ) -> None:
        """Initialize the agentic workflow."""
        # Sanitize kwargs to remove any BaseMessage objects before passing to super()
        sanitized_kwargs = {}
        try:
            from langchain_core.messages.base import BaseMessage
            for key, value in kwargs.items():
                if isinstance(value, BaseMessage):
                    sanitized_kwargs[key] = value.content if hasattr(value, 'content') else str(value)
                else:
                    sanitized_kwargs[key] = value
        except (ImportError, AttributeError):
            sanitized_kwargs = kwargs
        
        super().__init__(**sanitized_kwargs)
        self.index = index
        self.firecrawl_api_key = firecrawl_api_key
        
        if llm is not None:
            self.llm = llm
        else:
            # Fallback LLM - use the same model as main app (from env var or default)
            model = os.getenv("LLM_MODEL", "openrouter/openai/gpt-4o-mini")
            self.llm = LiteLLM(
                model=model,
                api_base="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )
        
        # Initialize agents
        retriever = self.index.as_retriever()
        self.retrieval_agent = RetrievalAgent("RetrievalAgent", self.llm, retriever)
        self.relevance_agent = RelevanceAgent("RelevanceAgent", self.llm)
        self.web_search_agent = WebSearchAgent("WebSearchAgent", self.llm, firecrawl_api_key)
        self.query_agent = QueryAgent("QueryAgent", self.llm)
        
        # Create orchestrator
        self.orchestrator = OrchestratorAgent(
            "Orchestrator",
            self.llm,
            {
                "retrieval": self.retrieval_agent,
                "relevance": self.relevance_agent,
                "web_search": self.web_search_agent,
                "query": self.query_agent
            }
        )
        
        from llama_index.core import Settings
        Settings.llm = self.llm
    
    @step
    async def process_query(self, ctx: Context, ev: StartEvent) -> StopEvent:
        """Process the query through the agentic workflow."""
        try:
            query_str = ev.get("query_str")
            
            if query_str is None:
                return StopEvent(result="No query provided.")
            
            print(f"DEBUG: Processing query: {query_str}")
            
            # Execute orchestrator
            print("DEBUG: Executing orchestrator...")
            result = await self.orchestrator.execute(query_str)
            
            print(f"DEBUG: Orchestrator result: {result}")
            
            return StopEvent(result=result.get("result", "No result generated."))
        except Exception as e:
            print(f"ERROR in process_query: {e}")
            import traceback
            traceback.print_exc()
            return StopEvent(result=f"Error processing query: {str(e)}")


