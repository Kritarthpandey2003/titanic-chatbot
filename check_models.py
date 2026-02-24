import os
from dotenv import load_dotenv
from google import genai

load_dotenv('C:/Users/Lenovo/.gemini/antigravity/scratch/titanic-chatbot/.env')
client = genai.Client()

print("Available models:")
try:
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print("Error:", e)
