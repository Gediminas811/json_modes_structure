import openai
import os
import json

from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print

# Load OpenAI key from .env
load_dotenv()

token = os.getenv("SECRET")  # Replace with your actual token
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

client = openai.OpenAI(
    api_key=token,
    base_url=endpoint)

question = input("Hello! Enter your question in Lithuanian: ")

class LithuanianQuestionCheck(BaseModel):
    is_lithuanian_language: bool

# Check if the question is in Lithuanian
response = client.beta.chat.completions.parse(
    model=model,    
    messages=[
        {"role": "system", "content": "You are a language detector. Respond in JSON: {'is_lithuanian_language': true/false}."},
        {"role": "user", "content": question}
    ],
    temperature=0.7,
    response_format=LithuanianQuestionCheck
)
# Parse structured result
if not response.choices or not response.choices[0].message.content:
    raise ValueError("Invalid response structure!")
content_str = response.choices[0].message.content
if content_str is None:
    raise ValueError("No content in response!")

content_dict = json.loads(content_str)
detected = LithuanianQuestionCheck.model_validate(content_dict)

# If Lithuanian, answer the question
if detected.is_lithuanian_language:
    print("Puiku! Atsakau: \n")
    answer = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "Atsakyk į klausimą lietuviškai."},
            {"role": "user", "content": question}
        ]
    )
    content = answer.choices[0].message.content
    if content is not None:
        print("Atsakymas:", content.strip())
    else:
        print("Atsakymas: (nėra atsakymo)")
else:
    print("Klausimas nėra lietuvių kalba, todėl neatsakysiu.")