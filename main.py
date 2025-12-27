
import google.generativeai as genai
from kaggle_secrets import UserSecretsClient
import time
import os
from PyPDF2 import PdfReader  

# 1. Setup API
user_secrets = UserSecretsClient()
api_key = user_secrets.get_secret("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. AUTOMATIC MODEL FINDER
# This looks at YOUR account and picks the names that actually exist
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

# We will pick the best available ones from your list
# From your previous check, we know these names are there
RESEARCH_MODEL = next((m for m in available_models if "pro" in m), available_models[0])
WRITER_MODEL = next((m for m in available_models if "flash" in m), available_models[0])

print(f"Using Research Model: {RESEARCH_MODEL}")
print(f"Using Writer Model: {WRITER_MODEL}")

def generate_with_gemini(prompt, model_name=WRITER_MODEL):
    time.sleep(5) # Avoid Rate Limit
    try:
        # Use the full name including 'models/' prefix from the list
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred with {model_name}: {e}"

print("\nSystem is now using confirmed model names from your account!")