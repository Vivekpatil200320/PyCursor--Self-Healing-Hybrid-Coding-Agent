import streamlit as st
import warnings
from langgraph.graph import StateGraph, START, END
from state_schema import AgentState
from nodes import coder_node, runner_node

warnings.filterwarnings("ignore") # Silences Python 3.14 warnings

st.set_page_config(page_title="PyCursor Pro", layout="wide")
st.title("🚀 PyCursor: The Self-Healing Agent")

# Sidebar Toggle
use_local = st.sidebar.toggle("Use Local Model (Ollama)", value=True)

# Graph Construction
workflow = StateGraph(AgentState)
workflow.add_node("coder", coder_node)
workflow.add_node("runner", runner_node)
workflow.add_edge(START, "coder")
workflow.add_edge("coder", "runner")

# Router Logic
def router(state):
    # Stop if success or if we hit 3 attempts
    if not state.get("error_log") or state.get("iteration", 0) >= 3:
        return END
    return "coder"

workflow.add_conditional_edges("runner", router)
app = workflow.compile()

if prompt := st.chat_input("Enter your vibe..."):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        code_box = st.empty()
        # INITIALIZE EVERY KEY HERE
        inputs = {
            "messages": [("user", prompt)],
            "iteration": 0,
            "error_log": "",
            "current_code": "",
            "use_local": use_local
        }
        
        for event in app.stream(inputs):
            for node, state in event.items():
                if node == "coder":
                    code_box.code(state.get("current_code", ""))
                if node == "runner" and state.get("error_log"):
                    st.error(f"Heal Attempt: {state['error_log']}")
                elif node == "runner":
                    st.success("Execution Successful!")