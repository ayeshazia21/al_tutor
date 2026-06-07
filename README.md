
AI Algorithm Tutor Agent
*Project Overview*

The AI Algorithm Tutor Agent is an intelligent educational system designed to help students understand fundamental and advanced algorithms through natural language interaction. Instead of relying on static textbooks or video lectures, the system functions as a conversational AI tutor that explains algorithms, analyzes code, extracts structured inputs, and dynamically computes time and space complexity.

The primary objective of this project is to bridge the gap between theoretical algorithm knowledge and interactive understanding by providing:

1) Step-by-step algorithm explanations
2)  Real-time time and space complexity analysis
3) Automatic detection of algorithms from natural language input
4) Execution-style reasoning through dry-run simulation
5) Context-aware follow-up conversations
6) Memory-based personalized learning experience

The system is built using a modular AI pipeline architecture, where each component performs a specialized cognitive function such as intent detection, reasoning, memory retrieval, planning, and response generation.

This makes the agent more than just a chatbot — it is a multi-layered AI tutoring system for algorithm education and problem-solving.


*System Architecture / Design*

The architecture of the AI Algorithm Tutor Agent follows a modular multi-layer pipeline design, integrating LLM-based reasoning, rule-based parsing, and memory-augmented retrieval systems.


1. User Interface Layer (Streamlit Frontend)

This layer handles all user interactions and serves as the entry point of the system.

Responsibilities:
Accept algorithm-related queries in natural language
Display structured AI-generated responses
Provide quick-action buttons (e.g., Bubble Sort, Quick Sort)
Render chat-based conversational interface
Show memory/history of interactions
Implementation:
Built using Streamlit

2. Agent Orchestration Layer (Core System Brain)

This is the central controller responsible for coordinating all system components.

Responsibilities:
Receives user queries from the UI
Manages workflow across all modules
Maintains conversation flow
Constructs dynamic prompts for the LLM
Returns final structured responses
Key File:
agent.py
Integrates:
Memory system
Router
Planner
Context resolver
Complexity analyzer
Array extraction module

3. Intent Detection & Routing Layer

This module interprets user input and converts it into structured intent.

Responsibilities:
Detect user intent (e.g., explain algorithm, dry run, analyze complexity)
Identify algorithm type (e.g., Bubble Sort, Merge Sort, BFS)
Extract numerical arrays from natural language input
Determine required output format
Technique:
LLM-based structured JSON parsing with rule-based fallback logic
Key File:
llm_router.py

4. Context Resolution Layer

Ensures smooth multi-turn conversation handling.

Responsibilities:
Detect follow-up queries (e.g., “continue”, “next step”)
Maintain active algorithm context
Resolve ambiguous references
Preserve conversational continuity
Key File:
context_resolver.py

5. Memory System (Short-Term + Long-Term)

The system implements a hybrid memory architecture.

Short-Term Memory

Stored in session state:

Chat history
Current algorithm context
Execution state of steps
UI state tracking

Long-Term Memory

Powered by ChromaDB vector database:

Stores embeddings of past interactions
Enables semantic retrieval of similar queries
Improves personalization over time
Key File:
vector_memory.py

6. Planning Layer

This module structures reasoning before generation.

Responsibilities:
Break down user queries into logical steps
Define explanation flow
Ensure structured teaching output
Improve clarity of responses
Key File:
planner.py

7. Complexity Analysis Module

A rule-based analytical engine for estimating algorithm complexity.

Responsibilities:
Detect loops and nested structures
Estimate time complexity (O(1), O(n), O(n²), etc.)
Estimate space complexity
Provide explanation for derived complexity
Technique:
Pattern recognition + loop depth analysis

8. Array Extraction Module
Extracts structured input arrays from natural language queries.

Example Inputs:
“Sort 9 2 7 1 5”
“Apply bubble sort on [10, 4, 2, 8]”
Output:
[9, 2, 7, 1, 5]
Purpose:
Enables dynamic algorithm simulation
Removes dependency on predefined inputs
Supports flexible user input formats

9. LLM Generation Layer

This is the final reasoning engine of the system.

Responsibilities:
Generate explanations
Produce pseudocode
Provide step-by-step reasoning
Adapt responses using memory + context
Model Used:
Llama 3.1 8B Instant (via Groq API)


 Overall System Workflow
User submits query via Streamlit UI
Agent core receives and processes input
Intent router classifies request and extracts entities
Context resolver checks for follow-up dependency
Memory system retrieves relevant past interactions
Planner structures reasoning steps
Complexity analyzer evaluates algorithm (if applicable)
Prompt is dynamically constructed
LLM generates structured response
Response is rendered in UI
Memory systems are updated (short-term + vector DB)
⚙️ Setup & Installation Instructions

Follow these steps carefully to run the project on your system:


1. Clone the Repository
git clone https://github.com/your-username/ai-algorithm-agent.git
cd ai-algorithm-agent

 2. Create Virtual Environment (Recommended)
Windows:
python -m venv venv
venv\Scripts\activate
Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application

If using Streamlit:

streamlit run ui/streamlit_app.py

If using Python entry file:

python main.py

5. Open in Browser

If Streamlit is used, open:

http://localhost:8501

Usage Guidelines

Once the system is running, you can interact with the AI agent as follows:


1. Ask Algorithm Questions

Examples:

“Explain Bubble Sort”
“What is Dijkstra’s Algorithm?”
“How does Binary Search work?”

2. Request Pseudocode

Examples:

“Give pseudocode for Merge Sort”
“Convert Quick Sort into pseudocode”
3. Code Generation

Examples:

“Write Python code for Heap Sort”
“Convert BFS into code”

4. Dry Run Mode

Examples:

“Dry run Bubble Sort on [5, 3, 2, 1]”
“Step-by-step execution of Binary Search”

5. Complexity Analysis

The agent provides:

Best case complexity
Average case complexity
Worst case complexity

Example:

“What is the time complexity of Merge Sort?”

6. Conversational Memory Usage

You can continue conversations naturally:

Example:

“Explain Quick Sort”
“Now give pseudocode”
“Do a dry run for [10, 2, 8, 1]”

The agent remembers context and responds accordingly.

Future Enhancements
Graph-based visualization of sorting algorithms
Step-by-step animation mode
Voice-based interaction
Multi-language code generation
AI-powered quiz system
Learning progress dashboard


Tech Stack
Python
Streamlit / UI Framework
NLP-based parsing (custom or LLM-based)
Data structures & algorithm engine
JSON / file-based memory system
📄 License

This project is intended for educational purposes.

🔗 Repository
https://github.com/your-username/ai-algorithm-agent
