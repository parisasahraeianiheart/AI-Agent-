from langgraph.graph import StateGraph, END
from osint_state import OSINTState

# === Import your agent functions ===
from agents.query_agent import query_analysis_agent
from agents.planning_agent import planning_agent
from agents.retrieval_agent import retrieval_agent
from agents.pivot_agent import pivot_agent
from agents.synthesis_agent import synthesize_report

# === Define the LangGraph pipeline ===
builder = StateGraph(OSINTState)

builder.add_node("QueryAnalysis", query_analysis_agent)
builder.add_node("Planning", planning_agent)
builder.add_node("Retrieval", retrieval_agent)
builder.add_node("Pivot", pivot_agent)
builder.add_node("Synthesis", synthesize_report)

# === Define the flow ===
builder.set_entry_point("QueryAnalysis")
builder.add_edge("QueryAnalysis", "Planning")
builder.add_edge("Planning", "Retrieval")
builder.add_edge("Retrieval", "Pivot")
builder.add_edge("Pivot", "Synthesis")
builder.add_edge("Synthesis", END)

# === Build the graph ===
osint_graph = builder.compile()