from dataclasses import dataclass

@dataclass
class TutorState:
    topic: str = None              # current algorithm (quicksort)
    stage: str = "idle"            # explain / example / complexity / compare / quiz
    subtopic: str = None           # pivot / partition / recursion
    awaiting_followup: bool = False
    last_user_intent: str = "explain"

    def reset(self):
        self.stage = "idle"
        self.awaiting_followup = False
        self.subtopic = None