# test_analyzer.py

from query_analyzer import analyze_query

queries = [
    "Explain Merge Sort",
    "Compare BFS and DFS",
    "Teach me search algorithms",
    "What is Dynamic Programming?",
    "Generate pseudocode for Dijkstra",
    "Why is Merge Sort O(n log n)?",
    "Give me interview questions on recursion"
]

for query in queries:

    print("\n===================================")
    print("QUERY:", query)

    result = analyze_query(query)

    print("\nANALYSIS:")
    print(result)

    print("===================================\n")