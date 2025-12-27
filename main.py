import os
import time
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# --- STEP 1: LOAD API KEY ---
# This loads your secret API key from the .env file
load_dotenv() 
api_key = os.getenv("GOOGLE_API_KEY") 

if not api_key:
    print("❌ ERROR: API Key not found in .env file!")
else:
    genai.configure(api_key=api_key)

# --- STEP 2: SELECT AI MODEL ---
# This finds the best available Gemini model in your account
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
BEST_MODEL = next((m for m in models if "1.5-flash" in m), models[0])
print(f"Using Model: {BEST_MODEL}")

# --- STEP 3: READ LOCAL DOCUMENTS ---
# This folder contains your course PDFs
DOCS_DIR = './my-documents' 

def get_context():
    text = ""
    if not os.path.exists(DOCS_DIR): 
        return "Folder 'my-documents' not found!"
    
    # Loop through every file in the folder
    for f in os.listdir(DOCS_DIR):
        p = os.path.join(DOCS_DIR, f)
        if f.endswith('.pdf'):
            try:
                # Extract text from PDF pages
                reader = PdfReader(p)
                text += f"\n[File: {f}]\n" + "".join([page.extract_text() for page in reader.pages if page.extract_text()])
            except: pass
        elif f.endswith('.txt'):
            # Read normal text files
            with open(p, 'r', encoding='utf-8') as file: 
                text += f"\n[File: {f}]\n" + file.read()
    return text[:20000] # Limit text size for the AI

# --- STEP 4: AGENT FUNCTION ---
# This function sends tasks to the AI and waits 30 seconds to avoid errors
def run_agent(role_name, task_prompt):
    print(f"🚀 {role_name} is starting its task...")
    time.sleep(30) # Wait 30 seconds so the API doesn't get busy
    try:
        model = genai.GenerativeModel(BEST_MODEL)
        response = model.generate_content(task_prompt)
        return response.text
    except Exception as e:
        return f"Error occurred: {e}"

# --- STEP 5: START THE MULTI-AGENT WORKFLOW ---
topic = "AI Agents in Education, Cybersecurity, and Healthcare"
context = get_context()

# Agent 1: The Researcher
research_prompt = f"Analyze these documents and find facts about {topic}:\n\n{context}"
research_data = run_agent("Researcher Agent", research_prompt)

# Agent 2: The Writer
writer_prompt = f"Write a long professional article using these facts: {research_data}"
draft = run_agent("Writer Agent", writer_prompt)

# Agent 3: The Editor
editor_prompt = f"Act as an Editor and fix the grammar of this article: {draft}"
final_article = run_agent("Editor Agent", editor_prompt)

# --- STEP 6: SAVE THE FINAL ARTICLE ---
with open('final_article.txt', 'w', encoding='utf-8') as f:
    f.write(final_article)

print("\n" + "="*40)
print("✅ MISSION COMPLETE: 'final_article.txt' is saved!")
print("="*40)