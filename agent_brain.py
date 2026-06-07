def build_agent_context(analysis: dict, memory: dict) -> str:

    intent = analysis.get("intent", "explain")
    topic = analysis.get("topic", "Unknown Topic")
    scope = analysis.get("scope", "concept")
    difficulty = analysis.get("difficulty", "medium")

    last_topic = memory.get("last_topic", None)

    return f"""
You are an Autonomous AI Tutor for Data Structures and Algorithms.

CURRENT TASK:
- Intent: {intent}
- Topic: {topic}
- Scope: {scope}
- Difficulty: {difficulty}

CONVERSATION MEMORY:
- Previous Topic: {last_topic}

CRITICAL RULES:
- If user answers a follow-up question, DO NOT reset context
- Always continue previous topic if relevant
- Never treat short replies like "yes/no/ok" as new topic
- Maintain continuity of teaching session
"""