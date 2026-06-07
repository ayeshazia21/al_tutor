from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DIFFICULTY_LEVELS = ["simple", "medium", "complex"]


def classify_difficulty(user_query: str, intent: str, algorithm: str) -> str:

    prompt = f"""
You are a strict classifier for algorithm tutoring difficulty.

Classify the user query into ONE of:

- simple: basic definition or short explanation
- medium: explanation with example
- complex: step-by-step + pseudocode + complexity

RULES:
- Output ONLY one word: simple, medium, or complex
- No explanation

User Query: {user_query}
Intent: {intent}
Algorithm: {algorithm}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    difficulty = response.choices[0].message.content.strip().lower()

    if difficulty not in DIFFICULTY_LEVELS:
        return "medium"

    return difficulty