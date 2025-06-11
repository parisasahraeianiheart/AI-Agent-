import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Load system prompt
with open("prompts/synthesis_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

def synthesize_report(state: dict) -> dict:
    findings = state.get("retrieval_results", [])
    if not findings:
        print("⚠️ No retrieval results to synthesize.")
        state["osint_report"] = "No data available for synthesis."
        return state

    # Just keep the essentials for synthesis
    essential_fields = ["title", "source", "confidence", "timestamp"]
    clean_findings = [
        {key: item[key] for key in essential_fields if key in item}
        for item in findings
    ]

    structured_findings = json.dumps(clean_findings, indent=2)

    user_prompt = f"""Here are the organized OSINT findings (in JSON format):

{structured_findings}

Please synthesize this into a concise, structured report that highlights:
- Key facts
- Risk indicators (if any)
- Public presence
- Summary of relevant affiliations or findings.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    report = response.content[0].text.strip()
    print("\n📄 Synthesized OSINT Report:\n", report)

    state["osint_report"] = report
    return state

# ✅ Optional test run
if __name__ == "__main__":
    dummy_state = {
        "retrieval_results": [
            {
                "title": "Ali Khaledi Nasab appointed as CEO of XYZ Corp",
                "source": "Reuters",
                "confidence": 0.8,
                "timestamp": 1717850000
            },
            {
                "title": "OFAC sanctions list – no match for Ali Khaledi Nasab",
                "source": "US Treasury",
                "confidence": 0.9,
                "timestamp": 1717850050
            }
        ]
    }

    result = synthesize_report(dummy_state)
    print("\n✅ Final Report in State:\n", result["osint_report"])