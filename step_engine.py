def get_algorithm_steps(topic: str):
    if topic == "Bubble Sort":
        return [
            "Compare adjacent elements",
            "Swap if left > right",
            "Move to next pair",
            "Repeat for full pass",
            "Repeat until sorted"
        ]

    elif topic == "Merge Sort":
        return [
            "Divide array into halves",
            "Recursively split",
            "Merge sorted halves",
            "Compare elements while merging",
            "Return final sorted array"
        ]

    elif topic == "Quick Sort":
        return [
            "Pick pivot",
            "Partition array",
            "Move smaller left, larger right",
            "Recursively sort partitions",
            "Combine results"
        ]

    return ["Explain concept"]