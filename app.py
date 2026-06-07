import streamlit as st
from agent import run_agent
from memory import AgentMemory
from database import initialize_database
from vector_memory import search_memory, get_all_memories, collection

# -----------------------------
# PAGE CONFIG (MUST BE FIRST)
# -----------------------------
st.set_page_config(
    page_title="AI Algorithm Assistant",
    page_icon="🧠",
    layout="wide"
)

# Set up database
initialize_database()

# Inject Clean UI Styles
st.markdown("""
<style>
    .chat-bubble-user { padding: 14px 18px; background-color: #2b303a; border-radius: 12px; margin-bottom: 12px; color: #f0f2f6; }
    .chat-bubble-agent { padding: 14px 18px; background-color: #0e1117; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = AgentMemory()

memory = st.session_state.memory

# -----------------------------
# SIDEBAR - ASSISTANT BRAIN & HISTORY
# -----------------------------
with st.sidebar:
    st.title("🧠 Assistant Settings")
    
    # Simple Reset Controls
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_btn2:
        if st.button("🗑️ Reset Brain", use_container_width=True):
            try:
                all_items = collection.get()
                all_ids = all_items.get("ids", [])
                if all_ids:
                    collection.delete(ids=all_ids)
                st.success("Brain memory cleared!")
            except Exception as e:
                st.error(f"Failed to reset: {e}")
                
    st.markdown("---")
    
    # Search Saved Knowledge
    st.subheader("🔍 Search Saved Lessons")
    query = st.text_input("Look up past concepts:", placeholder="e.g., Bubble Sort")
    
    if query:
        results = search_memory(query, k=3)
        st.markdown("##### Found Matches:")
        for i, r in enumerate(results):
            st.caption(f"**Match {i+1}:** {r}")
            
    st.markdown("---")
    
    # History Feed
    st.subheader("🧾 Recent Lessons")
    all_memories = get_all_memories(limit=5)
    for i, mem in enumerate(all_memories[::-1]):
        with st.expander(f"Saved Concept {i+1}"):
            st.write(mem["text"])

# -----------------------------
# MAIN APP INTERFACE LAYOUT
# -----------------------------
st.title("🧠 AI Algorithm Tutor")
st.caption("Learn algorithms, translate pseudocode, simulate execution, and check code efficiency.")
st.markdown("---")

# Split screen workspace layout - Given more width (3:2 ratio) to the chat area
left_col, right_col = st.columns([3, 2])

# ==========================================
# LEFT COLUMN: WIDE CHAT AREA
# ==========================================
with left_col:
    st.subheader("💬 Ask Questions Here")
    
    # Large Chat Window Frame
    chat_container = st.container(height=520, border=True)
    with chat_container:
        if not st.session_state.messages:
            st.info("Type an algorithm question or paste your code below to start learning!")
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-bubble-user'><b>🧑 You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble-agent'><b>🧠 Tutor:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    # Wide Text Input Box
    user_input = st.chat_input("Ask a question, request a code example, or describe an algorithm...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

    # Stream Response Processing
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        latest_query = st.session_state.messages[-1]["content"]
        
        with chat_container:
            st.markdown(f"<div class='chat-bubble-user'><b>🧑 You:</b><br>{latest_query}</div>", unsafe_allow_html=True)
            
            with st.spinner("Thinking..."):
                placeholder = st.empty()
                full_response = ""
                
                for token in run_agent(f"User Question: {latest_query}"):
                    full_response += token
                    placeholder.markdown(f"<div class='chat-bubble-agent'><b>🧠 Tutor:</b><br>{full_response}▌</div>", unsafe_allow_html=True)
                
                placeholder.markdown(f"<div class='chat-bubble-agent'><b>🧠 Tutor:</b><br>{full_response}</div>", unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

# ==========================================
# RIGHT COLUMN: THE TOOLBOX
# ==========================================
with right_col:
    st.subheader("🛠️ Algorithm Toolbox")
    
    # Simplified Quick-Action Tabs
    tab_pseudo, tab_dry, tab_complexity = st.tabs([
        "🔄 Pseudocode to Code", 
        "🧪 Run Simulation", 
        "📊 Speed & Memory Test"
    ])
    
    # TAB 1: PSEUDOCODE TRANSLATOR
    with tab_pseudo:
        st.markdown("### 🔄 Convert Plain Logic to Real Code")
        source_pseudo = st.text_area(
            "Paste your plain English steps or pseudocode here:", 
            value="Create an empty list\nLoop through each number in the input list\nIf the number is even, add it to our list", 
            height=140
        )
        target_lang = st.selectbox("Choose a programming language:", ["Python", "JavaScript", "C++", "Java"])
        
        if st.button("Generate Code", key="btn_pseudo"):
            with st.spinner("Writing clean code..."):
                translation_prompt = f"Convert this logic description into clean, well-commented code using {target_lang}:\n\n{source_pseudo}"
                compiled_code = ""
                for chunk in run_agent(translation_prompt):
                    compiled_code += chunk
                st.code(compiled_code, language=target_lang.lower())

    # TAB 2: DRY RUN / SIMULATION
    with tab_dry:
        st.markdown("### 🧪 Step-by-Step Code Simulation")
        target_code = st.text_area(
            "Paste the function code you want to test:", 
            value="def get_evens(numbers):\n    result = []\n    for n in numbers:\n        if n % 2 == 0:\n            result.append(n)\n    return result", 
            height=140
        )
        test_inputs = st.text_input("Enter sample data to test with:", value="[1, 2, 3, 4, 5]")
        
        if st.button("Simulate Steps", key="btn_dry"):
            with st.spinner("Simulating execution line by line..."):
                dry_run_prompt = f"Show a line-by-line dry run table showing how variables change for this code:\n{target_code}\nUsing these input parameters: {test_inputs}"
                trace_output = ""
                for chunk in run_agent(dry_run_prompt):
                    trace_output += chunk
                st.markdown(trace_output)

    # TAB 3: CODE COMPLEXITY
    with tab_complexity:
        st.markdown("### 📊 Speed and Memory Check")
        complexity_code = st.text_area(
            "Paste code here to see how well it scales:", 
            value="for item in items:\n    if item == target:\n        return True", 
            height=140
        )
        
        if st.button("Check Performance", key="btn_comp"):
            with st.spinner("Analyzing code loops and data structures..."):
                analysis_prompt = f"Analyze the performance of this code. Explain its Time Complexity (Speed) and Space Complexity (Memory usage) using easy-to-understand Big O notation language:\n\n{complexity_code}"
                asymptotic_output = ""
                for chunk in run_agent(analysis_prompt):
                    asymptotic_output += chunk
                st.markdown(asymptotic_output)