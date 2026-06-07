class ReferenceResolver:

    FOLLOW_UP_WORDS = [
        "elaborate", "explain more", "continue",
        "go deeper", "more detail"
    ]

    def resolve(self, query, memory):

        q = query.lower().strip()

        # 🔥 IMPORTANT: DO NOT OVERWRITE CONTEXT TOO MUCH
        if memory.awaiting_followup:
            if any(w in q for w in self.FOLLOW_UP_WORDS):
                return {
                    "query": query,   # keep original
                    "type": "followup"
                }

        if q in ["it", "this", "that"]:
            return {
                "query": memory.last_topic or query,
                "type": "reference"
            }

        return {
            "query": query,
            "type": "normal"
        }