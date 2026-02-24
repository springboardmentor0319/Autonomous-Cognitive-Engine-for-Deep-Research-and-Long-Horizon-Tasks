import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm=ChatOpenAI(model="gpt-4o-mini",temperature=0)

print(llm.invoke("Say hii!"))
history=[]


def clarify_or_answer(user_input: str):
    history.append(f"User:{user_input}")
    history_text="\n".join(history)
    prompt= f"""
you are an AI assistant.

User request:
"{user_input}"

Conversation so far:
{history}
If the request is missing important information:
-Ask ONE clear clarification question.

If the request is complete:
-Answer it directly.
"""
    result=llm.invoke(prompt)
    history.append(f"AI Agent:{result.content}")
    return result.content

while True:
    user_input = input("user: ")
    print("Agent:",clarify_or_answer(user_input))
