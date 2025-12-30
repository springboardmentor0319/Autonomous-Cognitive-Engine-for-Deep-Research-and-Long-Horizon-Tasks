import dotenv
dotenv.load_dotenv()
from langchain.chat_models import init_chat_model


model = init_chat_model("google_genai:models/gemini-2.5-flash")
response=model.invoke([{"role": "user", "content": "tell me what is gsoc?"}])
print(response)
