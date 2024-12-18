'''
A refactor for this:
https://medium.com/@cplog/introduction-to-langgraph-a-beginners-guide-14f9be027141
'''

from typing import Dict, TypedDict, Optional
from langgraph.graph import StateGraph, END

class GraphState(TypedDict, total=False):
    question: str
    classification: str
    response: str

def classify(question: str) -> str:
    return "greeting" if "hello" in question.lower() else "search"

def classify_input_node(state: GraphState) -> Dict:
    question = state.get('question', '').strip()
    classification = classify(question) 
    return {"classification": classification}

def handle_greeting_node(state: GraphState) -> Dict:
    return {"response": "Hello! How can I help you today?"}

def handle_search_node(state: GraphState) -> Dict:
    question = state.get('question', '').strip()
    search_result = f"Search result for '{question}'"
    return {"response": search_result}

def decide_next_node(state: GraphState) -> str:
    return "handle_greeting" if state.get('classification') == "greeting" else "handle_search"


workflow = StateGraph(GraphState)

workflow.add_node("classify_input", classify_input_node)
workflow.add_node("handle_greeting", handle_greeting_node)
workflow.add_node("handle_search", handle_search_node)

workflow.set_entry_point("classify_input")
workflow.add_conditional_edges(
    "classify_input",
    decide_next_node,
    {
        "handle_greeting": "handle_greeting",
        "handle_search": "handle_search"
    }
)
workflow.add_edge('handle_greeting', END)
workflow.add_edge('handle_search', END)

app = workflow.compile()
inputs = {"question": "Hello, how are you?"}
result = app.invoke(inputs)
print(result)