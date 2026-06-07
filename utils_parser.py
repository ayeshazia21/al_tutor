import re

def extract_array(text: str):
    """
    Extracts integer arrays from natural language input.
    Supports:
    - "9 2 7 1"
    - "[9,2,7,1]"
    - "array: 9 2 7 1"
    """

    if not text:
        return None

    # Case 1: [1,2,3]
    match = re.findall(r"\[([^\]]+)\]", text)
    if match:
        nums = match[0]
        return [int(x.strip()) for x in nums.split(",") if x.strip().isdigit()]

    # Case 2: numbers in sentence
    nums = re.findall(r"-?\d+", text)
    if nums:
        return [int(x) for x in nums]

    return None