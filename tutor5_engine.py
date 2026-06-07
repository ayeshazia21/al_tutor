class Tutor5:

    def __init__(self):
        self.current_topic = None
        self.mode = "TEACH"
        self.session_stage = 0

    def set_topic(self, topic):
        self.current_topic = topic
        self.mode = "TEACH"
        self.session_stage = 0

    def update_mode(self, mastery_score):

        if mastery_score < 0.3:
            self.mode = "SIMPLIFY"
        elif mastery_score < 0.6:
            self.mode = "TEACH"
        elif mastery_score < 0.85:
            self.mode = "PRACTICE"
        else:
            self.mode = "TEST"

    def next_stage(self):
        self.session_stage += 1