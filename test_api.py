# test_api.py

print("Script started...")

from dotenv import load_dotenv
import os
from groq import Groq

print("Imports loaded...")

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key found: {bool(api_key)}")

client = Groq(api_key=api_key)

print("Calling API...")

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": "Explain Binary Search in one sentence."}
        ]
    )
    print("Response received!")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")