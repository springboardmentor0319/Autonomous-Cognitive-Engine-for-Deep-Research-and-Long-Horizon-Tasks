import os
from dotenv import load_dotenv
from datetime import date

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()


@tool
def get_today_date() -> str:
    """Returns today's date"""
    return str(date.today())


@tool
def get_temperature(location: str) -> str:
    """Returns current temperature for a location (mock)"""
    return f"The current temperature in {location} is 30°C"


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general"
)

agent = create_agent(
    model,
    [tavily_search_tool, get_today_date, get_temperature]
)


def run_query(query: str):
    print("\n" + "=" * 80)
    print(f"USER QUESTION: {query}")
    print("=" * 80)

    for step in agent.stream(
        {"messages": query},
        stream_mode="values",
    ):
        msg = step["messages"][-1]
        if hasattr(msg, "content"):
            print("AI RESPONSE:")
            print(msg.content)


# 🔹 TEST 1: Tavily Search tool
run_query("What nation hosted the Euro 2024? Include only wikipedia sources.")

# 🔹 TEST 2: Date tool
run_query("What is today's date?")

# 🔹 TEST 3: Temperature tool
run_query("What is the temperature in Chennai?")

# 🔹 TEST 4: Multi-tool reasoning
run_query("Who hosted Euro 2024 and what is the temperature in Berlin?")
