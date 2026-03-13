import os, re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from tools.executor import run_python_code

load_dotenv()

def get_model(use_local=True):
    if use_local:
        # num_gpu=0 is the absolute fix for CUDA 500 crashes
        return ChatOllama(model="qwen2.5-coder:7b", temperature=0, num_gpu=0)
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

def coder_node(state: dict):
    # Defensive programming: provide defaults for every key
    messages = state.get("messages", [])
    iteration = state.get("iteration", 0)
    error = state.get("error_log", "")
    use_local = state.get("use_local", True)
    
    llm = get_model(use_local)
    
    # --- PLACING THE UPDATED PROMPT HERE ---
    sys_msg = (
        "You are a Senior Python Engineer. Write code in triple backticks.\n"
        "STRICT RULE: Never leave a 'try:' block empty. Always include 'pass' or logic.\n"
        "STRICT RULE: Ensure proper 4-space indentation for all blocks.\n"
        "No conversational text, only the code."
    )
    
    # If there was a previous error, we append it to the prompt
    if error:
        sys_msg += f"\n\n[FIX THIS ERROR FROM YOUR PREVIOUS ATTEMPT]:\n{error}"

    # The AI now sees the strict rules + the previous error
    resp = llm.invoke([("system", sys_msg)] + messages)
    
    # Regex extraction
    content = str(resp.content)
    code_match = re.search(r"```python\s*(.*?)\s*```", content, re.DOTALL)
    clean_code = code_match.group(1).strip() if code_match else content.strip()

    return {
        "messages": [resp], 
        "current_code": clean_code, 
        "iteration": iteration + 1
    }

    return {
        "messages": [resp], 
        "current_code": clean_code, 
        "iteration": iteration + 1
    }

def runner_node(state: dict):
    code = state.get("current_code", "")
    stdout, stderr = run_python_code(code)
    return {"error_log": stderr if stderr else ""}