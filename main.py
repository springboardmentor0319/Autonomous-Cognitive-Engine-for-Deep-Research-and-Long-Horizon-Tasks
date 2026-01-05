from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent

#Model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

#Tool
tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general"
)

#Create agent
agent = create_agent(
    model=model,
    tools=[tavily_search_tool]
)

#User query
query = "Explain autonomous cognitive engines with real-world examples"

#Run agent (streaming)
for step in agent.stream(
    {"messages": query},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
