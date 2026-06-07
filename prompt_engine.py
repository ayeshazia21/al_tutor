from prompts import get_reasoning_prompt


def build_prompt(intent: str, algorithm: str, difficulty: str) -> str:

    base_prompt = get_reasoning_prompt(intent, algorithm)

    dynamic_instruction = f"""

---  
🧠 DETECTED DIFFICULTY: {difficulty.upper()}

⚙️ RESPONSE RULES:

"""

    if difficulty == "simple":
        dynamic_instruction += """
- Give short explanation (5–7 lines)
- No steps needed
- No pseudocode unless explicitly asked
"""

    elif difficulty == "medium":
        dynamic_instruction += """
- Include explanation + one example
- Keep structure moderate
- Avoid full step-by-step breakdown
"""

    elif difficulty == "complex":
        dynamic_instruction += """
- Full structured breakdown required
- MUST include:
  - Step-by-step explanation
  - Example
  - Pseudocode (if applicable)
  - Complexity analysis
"""

    return base_prompt + dynamic_instruction