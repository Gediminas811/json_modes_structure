import openai
import os

from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print

load_dotenv()  # Load environment variables from .env file

token = os.getenv("SECRET")  # Replace with your actual token
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

# Homework 13: Lithuanian Language Question Answering System

# 1. User inputs a question.

user_input = input("Enter your question: ")

# Initialize the OpenAI client
client = openai.OpenAI(
    api_key=token,
    base_url=endpoint)

class LithuanianQuestionCheck(BaseModel):
    is_lithuanian_language: bool
    confidence_score: float

response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": """You are a helpful assistant. You accept user's question, determine if it's in Lithuanian language, 
and if so, provide an answer to the question using an OpenAI language model."""},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        response_format=LithuanianQuestionCheck
    )

print(response.choices[0].message.parsed)
