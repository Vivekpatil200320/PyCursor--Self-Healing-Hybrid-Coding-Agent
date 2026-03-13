PyCursor: Self-Healing Hybrid Coding Agent
PyCursor is an autonomous Python coding agent built with LangGraph and Ollama. It translates "vibes" (natural language descriptions) into functional, executed Python code. If the generated code fails, the agent enters a self-healing loop—analyzing the error, rewriting the logic, and re-executing until the "vibe" is achieved.

🚀 Key Features
Self-Healing Loop: Automatically catches IndentationError, SyntaxError, and NameError, feeding the traceback back into the LLM for immediate correction.

Hybrid Engine Switch: Toggle between Local Privacy (via Ollama & Qwen2.5-Coder) and Cloud Power (via Gemini 1.5 Flash).

Syntax Guard: Custom regex-based middleware that prevents common LLM formatting errors (like empty try: blocks).

Stateful Architecture: Built on LangGraph to manage complex cycles and decision-making branches.

🛠️ Tech Stack
Logic: Python, LangGraph, LangChain

AI Models: Qwen2.5-Coder-7B (Local), Gemini 1.5 Flash (Cloud)

Infrastructure: Ollama (Local LLM Serving)

UI: Streamlit

📂 Project Structure
Plaintext
PyCursor/
├── tools/
│   └── executor.py      # Secure subprocess execution & syntax cleaning
├── nodes.py             # Agent logic and LLM factory
├── state_schema.py      # TypedDict state management for LangGraph
└── app.py               # Streamlit dashboard and graph orchestration
⚡ Quick Start
Clone & Install:

Bash
git clone https://github.com/your-username/pycursor.git
pip install -r requirements.txt
Local Setup:

Install Ollama.

Run ollama pull qwen2.5-coder:7b.

Run:

Bash
streamlit run app.py
🎯 Academic Context
Developed as part of my Master of Computer Applications (Data Science). This project explores the intersection of Generative AI and Autonomous Infrastructure, specifically focusing on reducing the "hallucination-to-execution" gap in local LLMs.
