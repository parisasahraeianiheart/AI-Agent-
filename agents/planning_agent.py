import os
import json
import anthropic
from dotenv import load_dotenv

# Load Anthropic API key
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Load system prompt
with open("prompts/planning_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

def planning_agent(state: dict) -> dict:
    structured_query = state.get("query_analysis", {})
    user_prompt = f"Here is the structured OSINT query:\n```json\n{json.dumps(structured_query, indent=2)}\n```"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    raw = response.content[0].text.strip()

    # Remove code block wrappers if present
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[len("json"):].strip()

    print("🔍 Planning Agent Output:\n", raw)

    try:
        parsed = json.loads(raw)
        state["osint_tasks"] = parsed  # ✅ This makes retrieval work!
    except Exception as e:
        print("❌ Error parsing planning output:", e)
        state["osint_tasks"] = []

    return state

# ✅ Optional: run independently
if __name__ == "__main__":
    from query_agent import query_analysis_agent
    user_query = "Investigate Ali Khaledi Nasab's professional background and risk exposure"
    state = {
        "user_query": user_query,
        "query_analysis": query_analysis_agent(user_query)
    }
    state = planning_agent(state)
    print("\n📌 Final OSINT Tasks:\n", state["osint_tasks"])