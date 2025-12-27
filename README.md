# Multi-Agent-Content-Production-Studio
An AI team that reads my course documents to research, write, and edit professional articles automatically. It uses Python and Google Gemini to show how multiple AI agents can work together as a digital office.


# Multi-Agent Content Production Studio 🤖✍️

This project is an AI-powered system that automates the process of researching and writing professional articles from local documents. It uses a **Multi-Agent Workflow** where different AI agents collaborate to produce high-quality content.

## 🌟 Features
* **PDF Processing**: Automatically reads and extracts text from local PDF and TXT files using `PyPDF2`.
* **Sequential Multi-Agent Workflow**:
    1. **Researcher Agent**: Analyzes documents and extracts key facts.
    2. **Writer Agent**: Drafts a professional 1500-word article based on research.
    3. **Editor Agent**: Polishes the draft for technical accuracy and tone.
* **Rate-Limit Handling**: Includes built-in delays to manage Gemini API free-tier quotas (Error 429).
* **Security**: Uses environment variables (`.env`) to keep API keys private.

## 🛠️ Tech Stack
* **Language**: Python
* **LLM**: Google Gemini 1.5 Flash
* **Libraries**: `google-generativeai`, `PyPDF2`, `python-dotenv`

## 🚀 How to Run
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
