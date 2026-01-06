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

user_input = "What nation hosted the Euro 2024? Include only wikipedia sources."

for step in agent.stream(
    {"messages": user_input},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
