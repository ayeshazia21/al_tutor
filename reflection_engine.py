from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def reflect_on_answer(question, answer):
    prompt = f"""
You are a strict AI tutor evaluator.

Evaluate the following answer:

QUESTION:
{question}

ANSWER:
{answer}

Return ONLY JSON:
{{
  "score": 1-10,
  "correctness": "low/medium/high",
  "improvements": "short feedback",
  "missing_points": "what is missing"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content