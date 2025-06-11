from langgraph.graph import StateGraph
from agents.query_agent import query_analysis_agent
from agents.planning_agent import planning_agent
from agents.retrieval_agent import retrieval_agent
from agents.pivot_agent import pivot_agent
from agents.synthesis_agent import synthesize_report  
from osint_state import OSINTState

# 🧠 Create LangGraph StateGraph
osint_graph = StateGraph(OSINTState)

# 🔗 Add your agents as nodes
osint_graph.add_node("QueryAnalysis", query_analysis_agent)
osint_graph.add_node("Planning", planning_agent)
osint_graph.add_node("Retrieval", retrieval_agent)
osint_graph.add_node("Pivot", pivot_agent)
osint_graph.add_node("Synthesis", synthesize_report)

# 🔁 Define the flow
osint_graph.set_entry_point("QueryAnalysis")
osint_graph.add_edge("QueryAnalysis", "Planning")
osint_graph.add_edge("Planning", "Retrieval")
osint_graph.add_edge("Retrieval", "Pivot")
osint_graph.add_edge("Pivot", "Synthesis")

# ✅ Export graph
osint_graph = osint_graph.compile()