#agent.py

from dotenv import load_dotenv
import os
import streamlit as st
import re

from groq import Groq
from llm_router import route_query
from vector_memory import store_memory, search_memory
from planner import create_plan
from context_resolver import ContextAwareResolver
from agent_brain import build_agent_context
from memory import AgentMemory

from utils_parser import extract_array

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

memory = AgentMemory()
resolver = ContextAwareResolver()


# -----------------------------
# STREAM RESPONSE
# -----------------------------
def stream_agent_response(system_prompt, user_query):

    system_prompt = system_prompt[:3000]
    user_query = user_query[:600]

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        stream=True,
        temperature=0.7,
        max_tokens=900
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# -----------------------------
# SUMMARY
# -----------------------------
def summarize_memory(client, history):

    text = "\n".join(
        [f"{m['role'].upper()}: {m['content'][:150]}" for m in history[-10:]]
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Summarize conversation into key learning points for an AI tutor."
            },
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].message.content


# -----------------------------
# COMPLEXITY ANALYZER
# -----------------------------
def analyze_complexity(code: str):

    code = code.lower()

    max_depth = 0
    current_depth = 0

    for line in code.split("\n"):
        line = line.strip()

        if line.startswith("for ") or line.startswith("while "):
            current_depth += 1
            max_depth = max(max_depth, current_depth)

        if line == "" or "return" in line:
            current_depth = 0

    # TIME COMPLEXITY
    if max_depth == 1:
        time = "O(n)"
        reason = "Single loop over input"
    elif max_depth == 2:
        time = "O(n²)"
        reason = "Nested loops detected"
    elif max_depth == 3:
        time = "O(n³)"
        reason = "Triple nested loops"
    else:
        time = "O(n^k)"
        reason = "Multiple nested loops detected"

    # SPACE COMPLEXITY
    if "list" in code or "append" in code:
        space = "O(n)"
        space_reason = "Extra data structure used"
    else:
        space = "O(1)"
        space_reason = "No extra space used"

    return {
        "time": time,
        "space": space,
        "reason": reason + ". " + space_reason
    }


# -----------------------------
# MAIN AGENT
# -----------------------------
def run_agent(user_query: str):

    # STEP 1: CONTEXT RESOLUTION
    resolved_pack = resolver.resolve(user_query, memory)
    resolved_query = resolved_pack["query"]
    is_followup = resolved_pack["is_followup"]

    # STEP 2: COMPLEXITY DETECTION
    complexity_result = None
    if "for" in resolved_query or "while" in resolved_query:
        complexity_result = analyze_complexity(resolved_query)

    # STEP 3: ARRAY EXTRACTION
    extracted_array = extract_array(user_query)
    if not extracted_array:
        extracted_array = [5, 3, 8, 1, 2]

    # STEP 4: MEMORY SEARCH
    relevant_memories = search_memory(resolved_query, k=2)

    # STEP 5: ROUTING
    route = route_query(resolved_query)

    intent = route.get("intent", "general")
    topic = route.get("topic", memory.active_topic)

    if is_followup and memory.active_topic:
        intent = "continue"
        topic = memory.active_topic

    if complexity_result:
        intent = "analyze_complexity"

    analysis = {
        "intent": intent,
        "topic": topic,
        "difficulty": route.get("difficulty", "medium"),
        "array": extracted_array
    }

    # STEP 6: PLAN
    plan = create_plan(resolved_query, analysis)

    # STEP 7: HISTORY
    recent_history = memory.get_recent_history()[-4:]

    history_text = "\n".join(
        [f"{m['role']}: {m['content'][:120]}" for m in recent_history]
    )

    # STEP 8: SYSTEM PROMPT
    system_prompt = build_agent_context(analysis, {
        "last_topic": memory.active_topic,
        "summary": memory.summary
    })

    system_prompt += f"""

🧠 COMPLEXITY ANALYSIS:
{complexity_result if complexity_result else "Not detected"}

🧠 RELEVANT MEMORY:
{str(relevant_memories)[:300]}

🧠 ACTIVE TOPIC:
{memory.active_topic}

🧠 HISTORY:
{history_text}

🧠 MODE:
{intent}

🧠 PLAN:
{str(plan)[:200]}

🧠 EXTRACTED ARRAY:
{extracted_array}

INSTRUCTION:

- Explain clearly
- Use step-by-step reasoning
- If complexity is detected, explain time & space complexity
- If array is present, use it in examples
"""

    # STEP 9: STREAM OUTPUT
    full_response = ""

    for token in stream_agent_response(system_prompt, resolved_query):
        full_response += token
        yield token

    # STEP 10: MEMORY UPDATE
    memory.update(analysis, full_response, user_query)

    # STEP 11: SUMMARY UPDATE
    if len(memory.history) % 10 == 0:
        memory.summary = summarize_memory(client, memory.history)
        st.session_state.summary = memory.summary

    # STEP 12: VECTOR STORE
    store_memory(
        text=user_query + "\n" + full_response,
        metadata={
            "topic": topic,
            "intent": intent
        }
    )