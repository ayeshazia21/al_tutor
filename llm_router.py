from groq import Groq
import os
import json
import re

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# SAFE JSON PARSER
# -----------------------------
def safe_parse_json(text: str):
    if not text:
        return fallback_route()

    text = text.strip()

    # Try direct JSON parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON block from messy output
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return fallback_route()


# -----------------------------
# FALLBACK ROUTE
# -----------------------------
def fallback_route():
    return {
        "intent": "general",
        "algorithm": "none",
        "input_array": [],
        "difficulty": "medium",
        "needs_visualization": False
    }


# -----------------------------
# ROUTER FUNCTION
# -----------------------------
def route_query(query: str):

    system_prompt = """
You are an AI routing engine for an algorithm tutor.

Return ONLY valid JSON.

Format:
{
  "intent": "visualize_algorithm | explain_code | pseudocode_to_code | trace_code | run_algorithm | continue | general",
  "algorithm": "bubble_sort | merge_sort | quick_sort | insertion_sort | selection_sort | none",
  "input_array": [],
  "difficulty": "beginner | medium | advanced",
  "needs_visualization": true
}

RULES:
- Output ONLY JSON
- No explanations
- No markdown
- If unsure → use "general"
- Always detect arrays from user input
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.0,
        max_tokens=200
    )

    raw_output = response.choices[0].message.content

    return safe_parse_json(raw_output)