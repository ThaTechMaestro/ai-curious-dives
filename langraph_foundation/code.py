from typing import Dict, TypedDict, Optional
from langgraph.graph import StateGraph, END

class GraphState(TypedDict):
    question: Optional[str] = None
    classification: Optional[str] = None
    response: Optional[str] = None

def classify_input_node(state):
    question = state.get('question', '').strip()
    classification = classify(question)  # Assume a function that classifies the input
    return {"classification": classification}

def handle_greeting_node(state):
    return {"response": "Hello! How can I help you today?"}

def handle_search_node(state):
    question = state.get('question', '').strip()
    search_result = f"Search result for '{question}'"
    return {"response": search_result}



workflow = StateGraph(GraphState)

workflow.add_node("classify_input", classify_input_node)
workflow.add_node("handle_greeting", handle_greeting_node)
workflow.add_node("handle_search", handle_search_node)

def decide_next_node(state):
    return "handle_greeting" if state.get('classification') == "greeting" else "handle_search"

workflow.add_conditional_edges(
    "classify_input",
    decide_next_node,
    {
        "handle_greeting": "handle_greeting",
        "handle_search": "handle_search"
    }
)

workflow.set_entry_point("classify_input")
workflow.add_edge('handle_greeting', END)
workflow.add_edge('handle_search', END)

app = workflow.compile()
inputs = {"question": "Hello, how are you?"}
result = app.invoke(inputs)
print(result)