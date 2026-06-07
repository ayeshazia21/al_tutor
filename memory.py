#memory.py

import streamlit as st
from database import save_message, load_messages


class AgentMemory:
    def __init__(self):

        # -------------------------
        # CHAT HISTORY (DB + SESSION)
        # -------------------------
        if "history" not in st.session_state:
            st.session_state.history = load_messages()

        # -------------------------
        # SUMMARY MEMORY
        # -------------------------
        if "summary" not in st.session_state:
            st.session_state.summary = ""

        # -------------------------
        # TOPIC TRACKING
        # -------------------------
        if "active_topic" not in st.session_state:
            st.session_state.active_topic = None

        # -------------------------
        # STEP ENGINE (CORE UPGRADE)
        # -------------------------
        if "step_state" not in st.session_state:
            st.session_state.step_state = {
                "topic": None,
                "step_index": 0,
                "steps": [],
                "paused": False,
                "last_explained": None
            }

        # -------------------------
        # VISUALIZATION STATE
        # -------------------------
        if "visual_state" not in st.session_state:
            st.session_state.visual_state = {
                "array": None,
                "step": 0,
                "history": []
            }

        # bind to instance
        self.history = st.session_state.history
        self.summary = st.session_state.summary
        self.active_topic = st.session_state.active_topic
        self.step_state = st.session_state.step_state
        self.visual_state = st.session_state.visual_state

    # =========================================================
    # SUMMARY UPDATE
    # =========================================================
    def update_summary(self, new_text: str):
        if len(self.summary) < 1000:
            self.summary += "\n" + new_text
        else:
            self.summary = self.summary[-800:] + "\n" + new_text

        st.session_state.summary = self.summary

    # =========================================================
    # MESSAGE STORAGE (DB + SESSION)
    # =========================================================
    def add_message(self, role, content):

        self.history.append({
            "role": role,
            "content": content
        })

        # persist in SQLite
        save_message(role, content)

        # keep memory small
        if len(self.history) > 20:
            self.history = self.history[-20:]

        st.session_state.history = self.history

    # =========================================================
    # MAIN UPDATE FUNCTION
    # =========================================================
    def update(self, analysis, response, user_query):

        # store conversation
        self.add_message("user", user_query)
        self.add_message("assistant", response)

        # -------------------------
        # TOPIC UPDATE
        # -------------------------
        if analysis.get("topic"):
            self.active_topic = analysis["topic"]
            st.session_state.active_topic = self.active_topic

        # -------------------------
        # STEP ENGINE CONTROL
        # -------------------------
        if analysis.get("intent") == "continue":
            self.step_state["step_index"] += 1
        else:
            self.step_state["step_index"] = 0

        self.step_state["topic"] = self.active_topic
        self.step_state["last_explained"] = response[:200]

        st.session_state.step_state = self.step_state

        # -------------------------
        # SUMMARY UPDATE
        # -------------------------
        self.update_summary(response[:200])

        # safety step sync
        self.update_step(analysis)

    # =========================================================
    # HISTORY ACCESS
    # =========================================================
    def get_recent_history(self, n=6):
        return self.history[-n:]

    # =========================================================
    # STEP CONTROL (ENGINE LOGIC)
    # =========================================================
    def update_step(self, analysis):

        topic = analysis.get("topic")

        # NEW TOPIC → RESET ENGINE
        if topic != self.step_state["topic"]:
            self.step_state["topic"] = topic
            self.step_state["step_index"] = 0
            self.step_state["last_explained"] = None

        # CONTINUE → MOVE FORWARD
        elif analysis.get("intent") == "continue":
            self.step_state["step_index"] += 1

        st.session_state.step_state = self.step_state

    # =========================================================
    # VISUAL STATE HELPERS
    # =========================================================
    def reset_visual(self, array, steps):
        self.visual_state["array"] = array
        self.visual_state["history"] = steps
        self.visual_state["step"] = 0

        st.session_state.visual_state = self.visual_state

    def next_visual_step(self):
        if self.visual_state["step"] < len(self.visual_state["history"]) - 1:
            self.visual_state["step"] += 1

        st.session_state.visual_state = self.visual_state