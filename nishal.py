from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyAHssdhOL6DDzJQB4fmzRd0EUPR0wLHuRA"

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

response = model.invoke("tell me what is gsoc?")
print(response.content)


