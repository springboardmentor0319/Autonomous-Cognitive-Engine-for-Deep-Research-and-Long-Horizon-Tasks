from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_community.tools import ShellTool
import requests

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.2
)

tavily_client = TavilyClient()
@tool
def websearch(query: str) -> str:
    """Search the web using Tavily and return a plain-text result."""
    result = tavily_client.search(query=query)
    return str(result)



def _get_weather_impl(place: str) -> str:
    """Get a short weather summary from wttr.in (no API key required)."""
    resp = requests.get(
        f"https://wttr.in/{place}", params={"format": "3"}, headers={"User-Agent": "langchain-demo/1.0"}, timeout=10
    )
    resp.raise_for_status()
    return resp.text.strip()
 
@tool
def get_weather(place: str) -> str:
    """Return a short weather summary for `place` using wttr.in."""
    return _get_weather_impl(place)

@tool
def add(a: int, b: int):
    """
    Adds two numbers whcih are integers 
    Args   
    :param a: First integer
    :type a: int
    :param b: Second Integer
    :type b: int

    Response: Sum of two integers 
    """

    return a + b

@tool
def multiply(a:int, b:int) -> int:
    """
    Multiplies two integers
    
    :param a: First integer
    :type a: int
    :param b: Second integer
    :type b: int
    :return: Product of a and b
    :rtype: int
    """
    return a * b


shell_tool = ShellTool()
results = shell_tool.invoke('whoami')
print(results)

model_with_tools = llm.bind_tools([websearch, get_weather, add, multiply])

prompt = "What is 100 times 2?"
response = model_with_tools.invoke(prompt)
print(response)

place = "Pune"
print("Weather:", _get_weather_impl(place))