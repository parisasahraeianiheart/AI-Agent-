from osint_graph import osint_graph
from osint_state import OSINTState

if __name__ == "__main__":
    # 👤 Sample user query with structured query analysis
    state = OSINTState(
        user_query="Investigate the professional background, affiliations, and risk exposure of Ali Khaledi Nasab",
        query_analysis={
            "entities": ["Ali Khaledi Nasab"],
            "intent": "Investigate professional background and risk exposure",
            "goals": [
                "Determine past and current company affiliations",
                "Check for political or legal exposure",
                "Find related associates or business partners"
            ],
            "data_requirements": [
                "Employment history", "Corporate records", "Sanctions or criminal records"
            ],
            "priority_sources": ["LinkedIn", "Reuters", "US Treasury", "Company registries"]
        }
    )

    print("🚀 Invoking LangGraph workflow...")
    final_state = osint_graph.invoke(state)

    print("\n🧠 Final OSINT Report:\n")
    print(final_state.get("osint_report", "❌ No report found in final state"))