from memory import AgentMemory

m = AgentMemory()

print("Has last_topic:", hasattr(m, "last_topic"))
print("Has last_intent:", hasattr(m, "last_intent"))
print("Has last_difficulty:", hasattr(m, "last_difficulty"))