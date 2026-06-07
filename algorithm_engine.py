def bubble_sort_steps(arr):
    steps = []
    a = arr.copy()

    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):

            steps.append({
                "array": a.copy(),
                "action": f"Comparing {a[j]} and {a[j+1]}"
            })

            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

                steps.append({
                    "array": a.copy(),
                    "action": f"Swapped {a[j]} and {a[j+1]}"
                })

    steps.append({
        "array": a.copy(),
        "action": "Sorted array completed"
    })

    return steps


def merge_sort_steps(arr):
    steps = []

    def merge_sort(a, depth=0):
        if len(a) <= 1:
            return a

        mid = len(a) // 2
        left = merge_sort(a[:mid], depth + 1)
        right = merge_sort(a[mid:], depth + 1)

        steps.append({
            "array": left + right,
            "action": f"Merging {left} and {right}"
        })

        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        steps.append({
            "array": merged.copy(),
            "action": f"Merged into {merged}"
        })

        return merged

    merge_sort(arr)
    return steps


def quick_sort_steps(arr):
    steps = []
    a = arr.copy()

    def quicksort(low, high):
        if low < high:
            p = partition(low, high)
            quicksort(low, p - 1)
            quicksort(p + 1, high)

    def partition(low, high):
        pivot = a[high]
        i = low - 1

        steps.append({
            "array": a.copy(),
            "action": f"Pivot chosen: {pivot}"
        })

        for j in range(low, high):
            if a[j] < pivot:
                i += 1
                a[i], a[j] = a[j], a[i]

                steps.append({
                    "array": a.copy(),
                    "action": f"Swapped {a[i]} and {a[j]}"
                })

        a[i + 1], a[high] = a[high], a[i + 1]

        steps.append({
            "array": a.copy(),
            "action": f"Placed pivot {pivot}"
        })

        return i + 1

    quicksort(0, len(a) - 1)
    return steps


# 🧠 MASTER FUNCTION (IMPORTANT)
def generate_steps(algorithm: str, arr: list):
    if algorithm == "bubble_sort":
        return bubble_sort_steps(arr)

    elif algorithm == "merge_sort":
        return merge_sort_steps(arr)

    elif algorithm == "quick_sort":
        return quick_sort_steps(arr)

    else:
        return [{
            "array": arr,
            "action": "Algorithm not supported"
        }]