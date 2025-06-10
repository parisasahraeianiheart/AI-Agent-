import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Load prompt
with open("prompts/planning_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

def planning_agent(structured_query: dict) -> list:
    user_prompt = f"Here is the structured OSINT query:\n```json\n{json.dumps(structured_query, indent=2)}\n```"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    raw = response.content[0].text.strip()

    # Strip ```json if present
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[len("json"):].strip()

    print("🔍 Planning Agent Output:\n", raw)

    try:
        return json.loads(raw)
    except Exception as e:
        print("Error parsing planning output:", e)
        return []

# Test run
if __name__ == "__main__":
    from query_agent import query_analysis_agent
    query = "Investigate Ali Khaledi Nasab's professional background and risk exposure"
    structured_query = query_analysis_agent(query)
    tasks = planning_agent(structured_query)
    print("\n📌 Final OSINT Tasks:\n", tasks)