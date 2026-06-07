# planner.py

def create_plan(query: str, analysis: dict) -> str:

    intent = analysis.get("intent", "explain")
    topic = analysis.get("topic", "Unknown Topic")
    scope = analysis.get("scope", "concept")
    difficulty = analysis.get("difficulty", "medium")

    plan = f"""
1. Identify topic: {topic}
2. Determine intent: {intent}
3. Adjust explanation level: {difficulty}
4. Use scope-aware teaching: {scope}
5. Provide structured explanation + examples if needed
"""

    return plan