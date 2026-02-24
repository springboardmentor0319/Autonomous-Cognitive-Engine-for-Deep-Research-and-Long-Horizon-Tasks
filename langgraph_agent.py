from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    user_query: str
    clarification: Optional[str]
    is_ambiguous: bool
    answer: Optional[str]   # ✅ Added this


AMBIGUOUS_KEYWORDS = ["report", "design", "analysis", "plan"]


def detect_ambiguity(state: AgentState):
    query = state["user_query"].lower()

    for word in AMBIGUOUS_KEYWORDS:
        if word in query:
            return {
                "is_ambiguous": True,
                "clarification": None
            }

    return {
        "is_ambiguous": False,
        "clarification": None
    }


def ask_clarification(state: AgentState):
    query = state["user_query"].lower()

    if "report" in query:
        question = "What type of report do you want? (sales/academics/project)"
    elif "design" in query:
        question = "What kind of design are you looking for? (graphic/web/industrial)"
    elif "analysis" in query:
        question = "What type of analysis do you need? (data/financial/market)"
    elif "plan" in query:
        question = "What kind of plan do you want? (business/travel/fitness)"
    else:
        question = "Could you please provide more details?"

    
    print("AI Agent:", question)
    user_answer = input("User: ")

    return {
        "clarification": user_answer,
        "is_ambiguous": False
    }


def execute_task(state: AgentState):
    final_task = state["user_query"]
    clarification = state.get("clarification")

    if clarification:
        answer = f"Based on your request for '{final_task}' and the clarification '{clarification}', here is the detailed response."
    else:
        answer = f"Here is the detailed response to your request for '{final_task}'."

    return {
        "answer": answer
    }


graph = StateGraph[AgentState]()
graph.add_state("DetectAmbiguity", detect_ambiguity)
graph.add_state("AskClarification", ask_clarification)
graph.add_state("ProvideAnswer", execute_task)

graph.add_transition("DetectAmbiguity", "AskClarification", lambda state: state["is_ambiguous"])
graph.add_transition("DetectAmbiguity", "ProvideAnswer", lambda state: not state["is_ambiguous"])
graph.add_transition("AskClarification", "ProvideAnswer", lambda state: True)

graph.set_start_state("DetectAmbiguity")
graph.set_end_state("ProvideAnswer")


def run_agent(user_query: str):
    initial_state: AgentState = {
        "user_query": user_query,
        "clarification": None,
        "is_ambiguous": False,
        "answer": None   # ✅ Added this
    }

    final_state = graph.run(initial_state)
    return final_state.get("answer")


if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        response = run_agent(user_input)
        print("Agent:", response)
