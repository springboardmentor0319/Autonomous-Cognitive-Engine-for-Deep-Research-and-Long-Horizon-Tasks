import os
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent

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
    [tavily_search_tool]
)

user_input = "What nation hosted the Euro 2024? Include only wikipedia sources."

for step in agent.stream(
    {"messages": user_input},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
