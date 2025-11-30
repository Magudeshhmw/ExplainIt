import streamlit as st
import explainit_lib as glib
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="ExplainIt",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Advanced Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Reset & Font */
    .stApp {
        background-color: #0d1117; /* GitHub Dark Dimmed */
        font-family: 'Inter', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h1 {
        background: linear-gradient(135deg, #58a6ff 0%, #8b949e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        padding-bottom: 0.5rem;
    }
    
    .stMarkdown p {
        color: #8b949e;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Cards & Containers */
    .css-1r6slb0, .stExpander, div[data-testid="stExpander"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        transition: border-color 0.2s ease;
    }
    
    div[data-testid="stExpander"]:hover {
        border-color: #58a6ff;
    }
    
    /* Inputs */
    .stTextArea textarea {
        background-color: #0d1117;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3);
    }
    
    /* Buttons */
    .stButton button {
        background-color: #238636;
        color: #ffffff;
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s cubic-bezier(0.3, 0, 0.5, 1);
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #2ea043;
        border-color: #8b949e;
        transform: scale(1.02);
    }
    
    .stButton button:active {
        background-color: #238636;
        transform: scale(0.98);
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #58a6ff;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #8b949e;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
    
    /* Code Blocks */
    code {
        font-family: 'JetBrains Mono', monospace;
        color: #ff7b72;
        background-color: rgba(255, 123, 114, 0.1);
        padding: 0.2em 0.4em;
        border-radius: 6px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #238636;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/code-file.png", width=64)
    st.title("ExplainIt")
    st.markdown("### AI-Powered Code Analysis")
    st.info("Drop a diff or paste code to get instant explanations, commit messages, and test plans.")
    
    st.markdown("#### ⚙️ Settings")
    model_choice = st.selectbox("Model", ["Claude 3.7 Sonnet", "Claude 3.5 Sonnet", "Claude 3 Haiku"], index=0)
    st.caption(f"Currently using: {model_choice}")
    
    st.markdown("---")

# --- Main Content ---
st.title("ExplainIt")
st.markdown("#### 🚀 Transform Code Changes into Human Insights")

# Input Section
st.markdown("### 📥 Input Source")
input_col1, input_col2 = st.columns([2, 1], gap="large")

with input_col1:
    input_text = st.text_area(
        "Paste Code or Diff", 
        height=300, 
        placeholder="// Paste your code or 'git diff' output here...\nfunction example() {\n  console.log('Hello World');\n}"
    )

with input_col2:
    st.markdown("**Or Upload Files**")
    uploaded_files = st.file_uploader("Drag and drop files here", accept_multiple_files=True)
    
    st.markdown("---")
    generate_btn = st.button("✨ Generate Analysis", type="primary")

# Processing Logic
if generate_btn:
    # 1. Input Handler
    final_input_text = ""
    input_type = "Unknown"
    
    if uploaded_files:
        input_type = "Multiple Files"
        for uploaded_file in uploaded_files:
            try:
                content = uploaded_file.read().decode("utf-8")
                final_input_text += f"\n--- File: {uploaded_file.name} ---\n{content}\n"
            except Exception as e:
                st.error(f"Error reading {uploaded_file.name}: {e}")
    elif input_text:
        final_input_text = input_text
        # Detect type
        if "diff --git" in input_text or "--- a/" in input_text or "+++ b/" in input_text:
            input_type = "Unified Diff"
        else:
            input_type = "Raw Code"
    else:
        st.warning("⚠️ Please provide input via text or file upload.")
        st.stop()

    # Progress Bar & Spinner
    progress_text = "Analyzing code structure..."
    my_bar = st.progress(0, text=progress_text)
    
    try:
        # 2. Repository & Diff Analysis Agent
        my_bar.progress(20, text="Extracting change metadata...")
        analysis = glib.analyze_code(final_input_text, input_type)
        
        # 3. Code Explanation Agent
        my_bar.progress(40, text="Drafting human-friendly explanation...")
        explanation = glib.explain_code(final_input_text, analysis)
        
        # 4. Commit Message Generator Agent
        my_bar.progress(60, text="Generating commit message variations...")
        commits = glib.generate_commit_messages(final_input_text, analysis)
        
        # 5. Unit Test Suggestor Agent
        my_bar.progress(80, text="Brainstorming test scenarios...")
        tests = glib.suggest_tests(final_input_text, analysis)
        
        # Confidence Score
        confidence = glib.get_confidence_score(final_input_text)
        my_bar.progress(100, text="Analysis complete!")
        my_bar.empty()

        # Output Display
        st.markdown("---")
        
        # Dashboard-style Metrics
        st.subheader("📊 Analysis Overview")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Change Scope", analysis.get('change_scope', 'N/A'))
        with m2:
            st.metric("Files Changed", analysis.get('files_changed', 0))
        with m3:
            st.metric("Lines Added", f"+{analysis.get('lines_added', 0)}")
        with m4:
            st.metric("Lines Removed", f"-{analysis.get('lines_removed', 0)}")
            
        st.info(f"**Affected Components:** {', '.join(analysis.get('affected_components', []))}")
        
        # Detailed Sections with Icons
        st.markdown("### 📝 Detailed Insights")
        
        with st.expander("📖 **Change Explanation**", expanded=True):
            st.markdown(explanation)
            
        col_commit, col_test = st.columns(2, gap="medium")
        
        with col_commit:
            st.markdown("#### 💬 Commit Messages")
            st.markdown(commits)
            
        with col_test:
            st.markdown("#### 🧪 Suggested Test Plan")
            st.markdown(tests)
            
        # Confidence Footer
        st.markdown("---")
        if confidence > 0.8:
            st.success(f"**AI Confidence Score:** {confidence:.2f} (High)")
        elif confidence > 0.5:
            st.warning(f"**AI Confidence Score:** {confidence:.2f} (Moderate)")
        else:
            st.error(f"**AI Confidence Score:** {confidence:.2f} (Low)")
            
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
