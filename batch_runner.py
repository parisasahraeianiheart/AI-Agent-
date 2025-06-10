from agents.query_agent import query_analysis_agent
from agents.planning_agent import planning_agent
from agents.retrieval_agent import retrieval_agent
import time
import json

def run_full_pipeline(user_query):
    print("📨 User Query:", user_query)

    structured_query = query_analysis_agent(user_query)
    print("\n✅ Structured Query:")
    print(json.dumps(structured_query, indent=2))

    planning_output = planning_agent(structured_query)
    print("\n📋 Planning Output:")
    print(json.dumps(planning_output, indent=2))

    print("\n🔍 Starting Retrievals...\n")
    retrievals = []
    for task in planning_output:
        print(f"▶️ Retrieving for task: {task['task_type']} | {task['target']}")
        result = retrieval_agent(task)
        retrievals.append(result)
        time.sleep(2)  # throttle to avoid rate limiting

    print("\n✅ Retrieval Summary:")
    for r in retrievals:
        print(f"🔗 {r['task']['task_type']} → {len(r['results'])} results")

    return {
        "query": user_query,
        "structured_query": structured_query,
        "tasks": planning_output,
        "retrievals": retrievals
    }

if __name__ == "__main__":
    output = run_full_pipeline("Investigate Ali Khaledi Nasab’s professional background and possible risk indicators")

    with open("osint_report_raw.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\n📝 Raw OSINT data saved to: osint_report_raw.json")