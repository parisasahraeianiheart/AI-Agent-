import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Load system prompt
with open("prompts/judge_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

def judge_agent(report_md: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the final report:\n```markdown\n{report_md}\n```"}
        ],
        temperature=0.3,
        max_tokens=1024
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[len("json"):].strip()

    try:
        return json.loads(raw)
    except Exception as e:
        print("❌ Judge Agent failed to parse output:", e)
        return {}

# Test
if __name__ == "__main__":
    with open("final_intelligence_report.md", "r") as f:
        report = f.read()

    verdict = judge_agent(report)
    print("\n⚖️ Judge Agent Verdict:\n", json.dumps(verdict, indent=2))