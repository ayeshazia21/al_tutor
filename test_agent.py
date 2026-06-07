from agent import run_agent

history = []

test_queries = [
    "Explain Merge Sort",
    "Generate its pseudocode",
    "Explain it step by step",
    "Show me an example of DFS",
    "What is the time complexity of Quick Sort?"
]

for query in test_queries:

    print(f"\nQuery: {query}")

    response = run_agent(query)

    print(response)
    print("=" * 60)

    # add to memory
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": response})