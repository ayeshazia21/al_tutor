class ConceptGraph:
    def __init__(self):
        self.graph = {
            "bubble sort": {
                "prerequisites": ["arrays", "comparisons"],
                "next": ["selection sort", "insertion sort"],
                "concepts": ["swapping", "iterations", "complexity"]
            },
            "merge sort": {
                "prerequisites": ["recursion", "arrays"],
                "next": ["quick sort"],
                "concepts": ["divide and conquer", "merging"]
            }
        }

    def get_concepts(self, topic):
        return self.graph.get(topic.lower(), {})