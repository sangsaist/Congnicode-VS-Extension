import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Groq API configuration (OpenAI Compatible)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

client = None
if GROQ_API_KEY:
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
    )

def call_llm(prompt):
    """
    Sends the prompt to the Groq API and returns the parsed JSON response.
    """
    if not client:
        return {"error": "GROQ_API_KEY not found in environment."}

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a DSA expert. Always respond in valid JSON format only."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        result = json.loads(response.choices[0].message.content)
        print(f"DEBUG LLM RESPONSE: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        print(f"Groq API Error: {e}")
        return {"error": f"Groq Error: {str(e)}"}
