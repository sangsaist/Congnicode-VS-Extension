import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_groq_key():
    api_key = os.getenv("GROQ_API_KEY")
    base_url = "https://api.groq.com/openai/v1"

    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in .env file.")
        return

    print(f"Testing Groq API Key: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
    
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Say 'Groq is working!' if you can read this."}
            ]
        )
        print("✅ SUCCESS!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print("❌ FAILED!")
        print(f"Error Details: {str(e)}")

if __name__ == "__main__":
    test_groq_key()
