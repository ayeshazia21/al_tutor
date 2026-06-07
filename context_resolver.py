class ContextAwareResolver:

    def resolve(self, query, memory):
        q = query.lower().strip()

        # 🧠 FOLLOWUP WORDS
        followups = ["it", "this", "that", "elaborate", "explain more", "continue"]

        if any(word in q for word in followups):

            if memory.active_topic:
                return {
                    "query": f"{query} about {memory.active_topic}",
                    "is_followup": True
                }

        return {
            "query": query,
            "is_followup": False
        }