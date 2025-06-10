from langgraph.graph import StateGraph, END
from langgraph.prebuilt.tool_node import ToolNode
from typing import TypedDict, Annotated, List, Any
from agents.query_agent import query_analysis_agent
from agents.planning_agent import planning_agent
from agents.retrieval_agent import retrieval_agent
from agents.pivot_agent import pivot_agent
from agents.synthesis_agent import synthesize_report
from agents.judge_agent import judge_agent

# Define memory structure
class OSINTState(TypedDict):
    query: str
    structured_query: dict
    tasks: list
    retrievals: list
    pivot_tasks: list
    final_report: str
    judgment: dict

# Node definitions
def node_query(state: OSINTState) -> OSINTState:
    print("🎯 Running Query Agent...")
    structured = query_analysis_agent(state["query"])
    state["structured_query"] = structured
    return state

def node_planning(state: OSINTState) -> OSINTState:
    print("📋 Running Planning Agent...")
    tasks = planning_agent(state["structured_query"])
    state["tasks"] = tasks
    return state

def node_retrieval(state: OSINTState) -> OSINTState:
    print("🌐 Running Retrieval Agent...")
    retrievals = []
    for task in state["tasks"]:
        result = retrieval_agent(task)
        retrievals.append(result)
    state["retrievals"] = retrievals
    return state

def node_pivot(state: OSINTState) -> OSINTState:
    print("🔁 Running Pivot Agent...")
    pivots = pivot_agent(state["retrievals"])
    state["pivot_tasks"] = pivots
    return state

def node_synthesis(state: OSINTState) -> OSINTState:
    print("📝 Running Synthesis Agent...")
    report = synthesize_report(state["retrievals"])
    state["final_report"] = report
    return state

def node_judge(state: OSINTState) -> OSINTState:
    print("⚖️ Running Judge Agent...")
    judgment = judge_agent(state["final_report"])
    state["judgment"] = judgment
    return state

# Build the graph
builder = StateGraph(OSINTState)

builder.add_node("query_agent", node_query)
builder.add_node("plan", node_planning)
builder.add_node("retrieve", node_retrieval)
builder.add_node("pivot", node_pivot)
builder.add_node("synthesize", node_synthesis)
builder.add_node("judge", node_judge)

builder.set_entry_point("query_agent")
builder.add_edge("query_agent", "plan")
builder.add_edge("plan", "retrieve")
builder.add_edge("retrieve", "pivot")
builder.add_edge("pivot", "synthesize")
builder.add_edge("synthesize", "judge")
builder.add_edge("judge", END)

graph = builder.compile()