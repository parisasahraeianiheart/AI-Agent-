import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

response = client.messages.create(
    model="claude-3-opus-20240229",  # Latest Claude 3 production model
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "Hello Claude! What can you do?"}]
        }
    ]
)

print("✅ Claude 3 responded:")
print(response)