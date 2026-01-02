import os
import time
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# ================= PAGE CONFIG =================
# This sets up the tab title and icon you see in the browser
st.set_page_config(
    page_title="Multi-Agent Content Studio",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= CUSTOM CSS & UI POLISH =================
# This entire block is just HTML and CSS to make the app look beautiful.
# It doesn't affect the logic/AI, it just styles the buttons, headers, and fonts.
st.markdown("""
<style>
    /* Import Google Font (Inter) for a modern look */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Header Styling - The purple gradient box at the top */
    .main-header {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .main-header p {
        color: #E0E7FF !important;
        font-size: 1.1rem;
    }

    /* Card/Container Styling - Makes the expanders look like white cards */
    .stExpander {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    /* Button Styling - Makes the button purple and full width */
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }

    /* Agent Info Cards - The 3 grey boxes explaining the agents */
    .agent-box {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4F46E5;
        margin-bottom: 10px;
    }
    .agent-title {
        font-weight: 700;
        color: #1F2937;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .agent-desc {
        color: #4B5563;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ================= HEADER SECTION =================
# This displays the main title on the screen using the CSS we defined above
st.markdown("""
<div class="main-header">
    <h1>Multi-Agent Content Studio</h1>
    <p>🚀 Powered by RAG & Gemini AI Agents</p>
</div>
""", unsafe_allow_html=True)

# ================= AGENT OVERVIEW (Columns) =================
# We split the screen into 3 equal columns to show the agent details side-by-side
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title">🔍 Researcher</div>
        <div class="agent-desc">Extracts key facts & data from documents.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title">✍️ Writer</div>
        <div class="agent-desc">Drafts structured content based on facts.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title">📝 Editor</div>
        <div class="agent-desc">Refines grammar, tone, and clarity.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---") # Adds a horizontal line separator

# ================= LOAD API =================
# This loads your secret passwords (API keys) from the .env file
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

# If the key isn't found, stop everything and show an error
if not gemini_api_key:
    st.error("⚠️ Google API Key missing. Please check your .env file.")
    st.stop()

# Connect to Google's AI servers
genai.configure(api_key=gemini_api_key)

# ================= GEMINI MODEL =================
# We look for a model that supports 'generateContent' (like Gemini Pro)
models = [m.name for m in genai.list_models()
          if 'generateContent' in m.supported_generation_methods]
GEMINI_MODEL = models[0] # Pick the first available model

# ================= DOCUMENT LOADER =================
DOCS_DIR = "./my-documents"

# This function reads your files. It's the "RAG" part (Retrieval).
def get_context():
    text = ""
    # If the folder doesn't exist, return nothing
    if not os.path.exists(DOCS_DIR):
        return ""
    
    # Loop through every file in the folder
    for file in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, file)
        
        # If it's a PDF, we use PdfReader to extract text
        if file.endswith(".pdf"):
            reader = PdfReader(path)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
        
        # If it's a Text file, we just read it normally
        elif file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text += f.read()
    
    # We limit text to 20,000 characters so we don't overwhelm the AI
    return text[:20000]

# ================= AGENT FUNCTION =================
# This is the "Brain". It takes a role (like "Writer") and a prompt (instructions)
def run_agent(role, prompt):
    # Show a spinner animation on screen so the user knows it's working
    with st.spinner(f"🤖 {role} is working on your request..."):
        time.sleep(1) # Pause for 1 second just for visual effect
        
        # Call Google Gemini
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt).text
    return response

# ================= INPUT SECTION =================
st.subheader("Start a New Project")
topic = st.text_input(
    "What topic should the agents cover?",
    "AI Agents in Education, Healthcare, and Cybersecurity",
    help="Enter the main subject for the article generation."
)

# ================= PIPELINE =================
# This runs when you click the button
if st.button("🚀 Generate Content Now"):
    
    # STEP 1: LOAD DOCUMENTS
    # We use st.status to show a collapsible progress box
    with st.status("📂 Loading Knowledge Base...", expanded=True) as status:
        context = get_context()
        
        # If no text was found, show error and stop
        if len(context) < 200:
            status.update(label="⚠️ Error: No documents found!", state="error")
            st.error("Please add PDF or TXT files to the 'my-documents' folder.")
            st.stop()
        else:
            status.update(label="✅ Knowledge Base Loaded", state="complete", expanded=False)

    # STEP 2: RESEARCHER AGENT
    st.write("---")
    st.subheader("1. Research Phase")
    with st.expander("🔍 See Research Findings", expanded=True):
        # We tell the AI to look at the 'context' (your PDF text) and find facts about the 'topic'
        research = run_agent(
            "Researcher Agent",
            f"Extract key facts about {topic} from this text:\n{context}"
        )
        st.markdown(research)

    # STEP 3: WRITER AGENT
    st.subheader("2. Drafting Phase")
    with st.expander("✍️ See Draft Content", expanded=False):
        # The writer takes the facts from the Researcher and writes a draft
        draft = run_agent(
            "Writer Agent",
            f"Write content using only these facts:\n{research}"
        )
        st.markdown(draft)

    # STEP 4: EDITOR AGENT
    st.subheader("3. Editing Phase")
    with st.expander("📝 See Final Article", expanded=True):
        # The editor cleans up the draft
        final = run_agent(
            "Editor Agent",
            f"Improve grammar and clarity:\n{draft}"
        )
        st.markdown(final)

        st.success("✅ Content generation complete!")
        
        # Create a button to download the result as a text file
        st.download_button(
            "📥 Download Article",
            final,
            file_name="final_article.txt"
        )

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #9CA3AF; font-size: 14px;">
    Multi-Agent System | RAG Architecture | Google Gemini
</div>
""", unsafe_allow_html=True)
