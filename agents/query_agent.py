import os
import anthropic
import json
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize Claude client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Load system prompt
with open("prompts/query_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()
'''
def query_analysis_agent(user_query: str) -> dict:
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[
        {
        "role": "user",
        "content": [{"type": "text", "text": str(user_query)}]
        }
        ]
    )

    try:
        raw_text = "".join(block.text for block in response.content if block.type == "text").strip()

        # Remove triple backticks if present
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[len("json"):].strip()

        print("🔍 Cleaned Claude Response:\n", raw_text)
        return json.loads(raw_text)

    except Exception as e:
        print("Error parsing response:", e)
        return {"error": str(e)}
'''
def query_analysis_agent(state: dict) -> dict:
    # ✅ Use existing structured query if present
    if "query_analysis" in state and state["query_analysis"]:
        print("✅ Using pre-populated structured query.")
        return state

     
    user_query = state.get("user_query", "")
    if not user_query:
        print("⚠️ No user query found in state.")
        return {"error": "Missing user query."}

    # 🧠 Call Claude to analyze user query
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": user_query}]
            }
        ]
    )

    try:
        raw_text = "".join(block.text for block in response.content if block.type == "text").strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[len("json"):].strip()

        print("🔍 Cleaned Claude Response:\n", raw_text)
        state["query_analysis"] = json.loads(raw_text)
        return state

    except Exception as e:
        print("❌ Error parsing response:", e)
        return {"error": str(e)}
       
# Example use
if __name__ == "__main__":
    user_query = "Investigate the professional history and risk factors for Ali Khaledi Nasab"
    result = query_analysis_agent(user_query)
    print(result)