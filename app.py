import streamlit as st
from agent import run_agent
from memory import AgentMemory
from database import initialize_database
from vector_memory import search_memory, get_all_memories, collection

# -----------------------------
# PAGE CONFIG (MUST BE FIRST)
# -----------------------------
st.set_page_config(
    page_title="Cosmic Algorithm Station",
    page_icon="🌌",
    layout="wide"
)

# Set up database
initialize_database()

# Inject Deep Space Theme & Planet / Star Styled UI Elements
st.markdown("""
<style>
    /* Global Deep Space Background Modifications */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d1117 0%, #07090e 100%);
    }
    
    /* Cosmic Chat Bubble styling */
    .chat-bubble-user { 
        padding: 16px 20px; 
        background: linear-gradient(135deg, #2b1b4d 0%, #1a103c 100%); 
        border-radius: 16px; 
        margin-bottom: 14px; 
        color: #e0e6ed;
        border: 1px solid #4a2f85;
        box-shadow: 0 4px 10px rgba(74, 47, 133, 0.2);
    }
    .chat-bubble-agent { 
        padding: 16px 20px; 
        background: linear-gradient(135deg, #0b192c 0%, #050d1a 100%); 
        border: 1px solid #1e3a5f; 
        border-radius: 16px; 
        margin-bottom: 14px;
        box-shadow: 0 4px 10px rgba(30, 58, 95, 0.2);
    }
    
    /* Planet & Star Styled Action Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #ff7b00 0%, #ffae00 100%) !important; /* Planet Magma theme */
        color: #07090e !important;
        font-weight: bold !important;
        border-radius: 50px !important; /* Circular/Planetoid shape */
        border: 2px solid #fff3cc !important;
        box-shadow: 0 0 15px rgba(255, 174, 0, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    div.stButton > button:hover {
        transform: scale(1.04) rotate(1deg);
        box-shadow: 0 0 25px rgba(255, 174, 0, 0.7) !important;
        border-color: #ffffff !important;
    }
    
    /* Alternate Star Styled Buttons for Utilities */
    .sidebar div.stButton > button {
        background: linear-gradient(135deg, #8a2be2 0%, #4a00e0 100%) !important; /* Supernova purple */
        color: #ffffff !important;
        border-radius: 20px !important;
        border: 1px solid #bd93f9 !important;
        box-shadow: 0 0 10px rgba(138, 43, 226, 0.4) !important;
    }
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
# SIDEBAR - KNOWLEDGE BASE ARCHIVE
# -----------------------------
with st.sidebar:
    st.title("🌌 Algorithm Memory")
    st.caption("Manage AI Memory and System Baselines")
    
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
    st.subheader("🪐 Scan Knowledge Base")
    query = st.text_input("Look up past concepts:", placeholder="e.g., Quick Sort")
    
    if query:
        results = search_memory(query, k=3)
        st.markdown("##### Found Matches:")
        for i, r in enumerate(results):
            st.caption(f"**Match {i+1}:** {r}")
            
    st.markdown("---")
    
    # History Feed
    st.subheader("📜 Logged Lessons")
    all_memories = get_all_memories(limit=5)
    for i, mem in enumerate(all_memories[::-1]):
        with st.expander(f"Saved Concept {i+1}"):
            st.write(mem["text"])

# -----------------------------
# MAIN APP PLACEMENT
# -----------------------------
st.title("🌌  Algorithm Generation and Explanation")
st.caption("Navigate algorithmic structures across the space framework.")
st.markdown("---")

# Separation of structural UI components into wide, clean high-level tabs
main_tab_tutor, main_tab_toolbox = st.tabs([
    "💬 🪐 AI Algorithm Tutor ", 
    "🛠️ 🚀 Algorithm Toolbox"
])

# ==========================================
# MAIN TAB 1: THE WIDE INTERACTIVE TUTOR TERMINAL
# ==========================================
with main_tab_tutor:
    st.subheader("💬 Ask Your Algorithm Questions")
    
    # Extra large frame optimized for broad code reads
    chat_container = st.container(height=580, border=True)
    with chat_container:
        if not st.session_state.messages:
            st.info("Broadcast an algorithm query or paste script code sequences to initiate tracking...")
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-bubble-user'><b>🧑 Explorer:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble-agent'><b>🧠 Tutor Core:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    # Wide Text Input Area Focus
    user_input = st.chat_input("Input mathematical queries or algorithm code expressions...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

    # Dynamic Agent Generation Block (Fixed logic looping)
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        latest_query = st.session_state.messages[-1]["content"]
        
        with chat_container:
            # FIX: Removed the explicit user-bubble display block here to resolve the duplication bug
            with st.spinner("Connecting to core logic clusters..."):
                placeholder = st.empty()
                full_response = ""
                
                for token in run_agent(f"User Question: {latest_query}"):
                    full_response += token
                    placeholder.markdown(f"<div class='chat-bubble-agent'><b>🧠 Tutor Core:</b><br>{full_response}▌</div>", unsafe_allow_html=True)
                
                placeholder.markdown(f"<div class='chat-bubble-agent'><b>🧠 Tutor Core:</b><br>{full_response}</div>", unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

# ==========================================
# MAIN TAB 2: SEPARATED ALGORITHM TOOLBOX
# ==========================================
with main_tab_toolbox:
    st.subheader("🛠️ Simulation Engine")
    
    # Secondary tool task tabs
    tab_pseudo, tab_dry, tab_complexity = st.tabs([
        "🔄 Pseudocode to Code Converter", 
        "🧪 Step-by-Step Code Simulator", 
        "📊 Speed & Memory Boundaries"
    ])
    
    # SUB-TAB 1: PSEUDOCODE TRANSLATOR
    with tab_pseudo:
        st.markdown("### 🔄 Convert Logic Abstractions to Executable Code")
        source_pseudo = st.text_area(
            "Paste your step sequence or pseudocode strings below:", 
            value="Create an empty list\nLoop through each number in the input list\nIf the number is even, add it to our list", 
            height=160
        )
        target_lang = st.selectbox("Select Target Language System:", ["Python", "JavaScript", "C++", "Java"])
        
        if st.button("🌟 Generate Target Code", key="btn_pseudo"):
            with st.spinner("Compiling logic pathways..."):
                translation_prompt = f"Convert this logic description into clean, well-commented code using {target_lang}:\n\n{source_pseudo}"
                compiled_code = ""
                for chunk in run_agent(translation_prompt):
                    compiled_code += chunk
                st.code(compiled_code, language=target_lang.lower())

    # SUB-TAB 2: DRY RUN / SIMULATION
    with tab_dry:
        st.markdown("### 🧪 Operational Register Variable Simulator")
        target_code = st.text_area(
            "Provide the code object method framework to isolate:", 
            value="def get_evens(numbers):\n    result = []\n    for n in numbers:\n        if n % 2 == 0:\n            result.append(n)\n    return result", 
            height=160
        )
        test_inputs = st.text_input("Configure Input Parameter State Data:", value="[1, 2, 3, 4, 5]")
        
        if st.button("🪐 Launch Step Trace", key="btn_dry"):
            with st.spinner("Processing local tracking variables..."):
                dry_run_prompt = f"Show a line-by-line dry run table showing how variables change for this code:\n{target_code}\nUsing these input parameters: {test_inputs}"
                trace_output = ""
                for chunk in run_agent(dry_run_prompt):
                    trace_output += chunk
                st.markdown(trace_output)

    # SUB-TAB 3: CODE COMPLEXITY
    with tab_complexity:
        st.markdown("### 📊 Structural Scale Performance Evaluation")
        complexity_code = st.text_area(
            "Paste target function loops to inspect depth weights:", 
            value="for item in items:\n    if item == target:\n        return True", 
            height=160
        )
        
        if st.button("💥 Test Performance Metrics", key="btn_comp"):
            with st.spinner("Evaluating loop layers and memory pointers..."):
                analysis_prompt = f"Analyze the performance of this code. Explain its Time Complexity (Speed) and Space Complexity (Memory usage) using easy-to-understand Big O notation language:\n\n{complexity_code}"
                asymptotic_output = ""
                for chunk in run_agent(analysis_prompt):
                    asymptotic_output += chunk
                st.markdown(asymptotic_output)