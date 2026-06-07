from tutor_state import TutorState

class TutorStateEngine:

    def next_state(self, memory, analysis, user_query):

        q = user_query.lower().strip()

        current = memory.get_state()

        # -------------------------
        # 1. USER GIVES ANSWER / FOLLOW-UP
        # -------------------------
        if current == "questioning":
            if q in ["yes", "ok", "continue", "explain more", "elaborate"]:
                return TutorState.DEEP_DIVE.value
            return TutorState.EXPLAINING.value

        # -------------------------
        # 2. USER ASKED NEW TOPIC
        # -------------------------
        if analysis["intent"] == "explain":
            return TutorState.EXPLAINING.value

        # -------------------------
        # 3. USER ASKED FOR DETAILS
        # -------------------------
        if analysis["intent"] in ["example", "step_by_step"]:
            return TutorState.DEEP_DIVE.value

        # -------------------------
        # DEFAULT
        # -------------------------
        return TutorState.EXPLAINING.value