import os
import json
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def synthesize_report(retrievals: list) -> str:
    input_text = json.dumps(retrievals, indent=2)

    system_prompt = """You are a professional intelligence analyst synthesizing OSINT data.

You will receive a structured JSON list of retrieval results from an OSINT investigation.

Write a clean, executive-style intelligence report, organized with:
1. Executive Summary
2. Key Findings
3. Risk Indicators
4. Entity Relationships
5. Contradictions or Gaps
6. Source Attribution and Confidence Scores

Use clear, professional language. Do not invent information beyond the provided evidence."""

    print("🧠 Synthesizing report using GPT-4o...")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here are the OSINT retrievals:\n```json\n{input_text}\n```"}
        ],
        temperature=0.4,
        max_tokens=4096
    )

    return response.choices[0].message.content.strip()
# Run + Save
if __name__ == "__main__":
    with open("osint_report_raw.json", "r") as f:
        data = json.load(f)
        retrievals = data["retrievals"]

    report = synthesize_report(retrievals)

    with open("final_intelligence_report.md", "w") as f:
        f.write(report)

    print("\n✅ Report generated and saved to: final_intelligence_report.md")