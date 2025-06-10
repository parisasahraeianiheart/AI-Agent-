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

def query_analysis_agent(user_query: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_query}]
    )

    try:
        raw_text = response.content[0].text.strip()

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

# Example use
if __name__ == "__main__":
    user_query = "Investigate the professional history and risk factors for Ali Khaledi Nasab"
    result = query_analysis_agent(user_query)
    print(result)