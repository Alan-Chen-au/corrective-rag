from langgraph.graph import StateGraph
from langgraph.graph import END
from typing_extensions import TypedDict
from typing import Literal

# -------------------------------
# Define state schemas
# -------------------------------

class GraphState(TypedDict):
    question: str
    result: str

# -------------------------------
# Define Nodes
# -------------------------------

def retrieve(state: GraphState) -> GraphState:
    return {"result": f"Retrieved answer for: {state['question']}"}

def web_search(state: GraphState) -> GraphState:
    return {"result": f"Searched the web for: {state['question']}"}

def grade_documents(state: GraphState) -> GraphState:
    return {"result": f"Graded: {state['result']}"}

# -------------------------------
# Define Router Function
# -------------------------------

def route_question(state: GraphState) -> Literal["WEBSEARCH", "RETRIEVE"]:
    if "internet" in state["question"].lower():
        return "WEBSEARCH"
    else:
        return "RETRIEVE"

# -------------------------------
# Build the Graph
# -------------------------------

builder = StateGraph(GraphState)

builder.add_node("RETRIEVE", retrieve)
builder.add_node("WEBSEARCH", web_search)
builder.add_node("GRADE", grade_documents)

# Conditional entry point: router chooses between two paths
builder.set_conditional_entry_point(
    route_question,
    {
        "RETRIEVE": "RETRIEVE",
        "WEBSEARCH": "WEBSEARCH"
    }
)

# After either RETRIEVE or WEBSEARCH, go to GRADE
builder.add_edge("RETRIEVE", "GRADE")
builder.add_edge("WEBSEARCH", "GRADE")
builder.add_edge("GRADE", END)

# The graph begins at the router
# builder.set_entry_point(route_question)

# -------------------------------
# Compile the workflow
# -------------------------------

app = builder.compile()

# -------------------------------
# Run it!
# -------------------------------

# print(app.invoke({"question": "What is AI?"}))
# -> Uses retrieve

print(app.invoke({"question": "Find the latest news on AI using the internet."}))
# -> Uses web_search
