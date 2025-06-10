import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Load system prompt
with open("prompts/pivot_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

def pivot_agent(retrievals: list) -> dict:
    prompt = f"""You are the Pivot Agent in an OSINT pipeline.

Your goals are:
1. Analyze the retrieved results to extract **new related entities** (e.g., new people, organizations, companies).
2. Detect **inconsistencies** or **conflicting information** between different sources.
3. Generate **follow-up search tasks** for:
   - New entities
   - Any inconsistencies that require resolution
   - Unanswered data requirements (e.g., missing info)

Return a JSON object with three keys:
- "new_entities": list of new entities and their type
- "inconsistencies": list of conflicting facts across sources
- "follow_up_tasks": list of dicts with task_type, target, source, priority, reason

Here is the retrieved OSINT content:
```json
{json.dumps(retrievals, indent=2)}
```"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=2048
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[len("json"):].strip()

    try:
        return json.loads(raw)
    except Exception as e:
        print("❌ Error parsing Pivot Agent output:", e)
        return {
            "new_entities": [],
            "inconsistencies": [],
            "follow_up_tasks": []
        }

# Test run
if __name__ == "__main__":
    with open("osint_report_raw.json", "r") as f:
        data = json.load(f)
        retrievals = data["retrievals"]

    pivot_output = pivot_agent(retrievals)
    print("\n🔁 Pivot Agent Output:\n", json.dumps(pivot_output, indent=2))