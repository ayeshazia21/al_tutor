def analyze_query(query: str, memory):
    text = query.lower()

    # -----------------------------
    # 🧠 FOLLOW-UP OVERRIDE (HIGHEST PRIORITY)
    # -----------------------------
    step_triggers = [
        "next", "continue", "go on", "proceed",
        "step", "what's next", "resume"
    ]

    is_continue = any(p in text for p in step_triggers)

    if is_continue and memory.active_topic:
        return {
            "intent": "continue",
            "topic": memory.active_topic,
            "scope": "step",
            "difficulty": "medium"
        }

    # -----------------------------
    # 🧠 INTENT DETECTION (MAIN LOGIC)
    # -----------------------------
    if any(k in text for k in ["pseudocode", "convert to code", "write code"]):
        intent = "pseudocode_to_code"

    elif any(k in text for k in ["explain this code", "what does this code do", "explain code"]):
        intent = "explain_code"

    elif any(k in text for k in ["dry run", "trace", "step by step execution"]):
        intent = "trace_code"

    elif any(k in text for k in ["visual", "show steps", "visualize"]):
        intent = "visualize_algorithm"

    elif any(k in text for k in ["sort", "bubble", "merge", "quick"]):
        intent = "run_algorithm"

    else:
        intent = "general"

    # -----------------------------
    # 🧠 TOPIC DETECTION
    # -----------------------------
    if "bubble" in text:
        topic = "Bubble Sort"

    elif "merge" in text:
        topic = "Merge Sort"

    elif "quick" in text:
        topic = "Quick Sort"

    else:
        topic = memory.active_topic or "General Algorithm"

    # -----------------------------
    # 🧠 FINAL OUTPUT
    # -----------------------------
    return {
        "intent": intent,
        "topic": topic,
        "scope": "adaptive",
        "difficulty": "medium"
    }