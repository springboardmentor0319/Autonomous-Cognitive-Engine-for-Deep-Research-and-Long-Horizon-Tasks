from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from groq import Groq
import os

# Groq client (NO LangChain)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# State
class AgentState(TypedDict):
    messages: List[dict]   # [{"role": "user"/"assistant", "content": "..."}]

# Agent Node
def clarifying_agent(state: AgentState):
    system_prompt = {
        "role": "system",
        "content": """
You are a smart clarifying assistant.

Rules:
1. If the user's query is incomplete or ambiguous, ask ONE clear follow-up question.
2. If the query has enough detail, give the final helpful answer.
3. Do NOT ask unnecessary questions.
4. Do NOT repeat questions already answered.
5. Be concise and natural.
"""
    }

    messages = [system_prompt] + state["messages"]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0
    )

    assistant_reply = response.choices[0].message.content

    state["messages"].append({
        "role": "assistant",
        "content": assistant_reply
    })

    return state

# LangGraph Setup
graph = StateGraph(AgentState)

graph.add_node("agent", clarifying_agent)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

app = graph.compile()

# Run Loop
if __name__ == "__main__":
    print("\nClarifying Agent (LangGraph + Groq SDK only, no LangChain)\n")

    state = {"messages": []}

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        state["messages"].append({
            "role": "user",
            "content": user_input
        })

        state = app.invoke(state)

        print("Agent:", state["messages"][-1]["content"])
        print()