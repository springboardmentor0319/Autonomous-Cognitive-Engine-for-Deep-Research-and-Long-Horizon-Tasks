import dotenv
dotenv.load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)
response=model.invoke([{"role": "user", "content": "what is gsoc?"}])
print(response.content)