from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.tools import tool

# Model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# Web Search Tool
tavily_search_tool = TavilySearch(
    max_results=3,
    topic="general"
)
@tool
def web_search(query: str) -> str:
    """web_search tool"""
    result = tavily_search_tool.invoke({"query": query})
    return str(result)

# Current Time Tool
@tool
def get_current_time() -> str:
    """Returns the current system date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Weather Tool
@tool
def get_weather(city: str, date: str) -> str:
    """Returns weather information for a given city and date."""
    return f"The weather in {city} on {date} is expected to be sunny."

# Create agent
agent = create_agent(
    model=model,
    tools=[web_search, get_current_time, get_weather]
)

# User query
query = "What is the current time? what will be the weather in Delhi tomorrow? Why do parrots talk?"

#Run agent
response = agent.invoke({"messages": query})
print(response)
