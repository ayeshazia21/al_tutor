def format_response(intent: str, algorithm: str, raw_response: str) -> str:

    return f"""

🧠 AI ALGORITHM TUTOR (REASONING MODE)


📌 Algorithm: {algorithm}
🎯 Task: {intent}


{raw_response}


"""