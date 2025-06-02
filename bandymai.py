import os
import json
import openai
from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print

# Load API key
load_dotenv()
token = os.getenv("SECRET")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

# OpenAI client
client = openai.OpenAI(api_key=token, base_url=endpoint)

# Define validation model
class LithuanianQuestionCheck(BaseModel):
    is_lithuanian_language: bool

# Get user input
question = input("Hello! Enter your question in Lithuanian: ")

# Step 1: Language detection
response = client.beta.chat.completions.parse(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a language detector. Respond in JSON: {'is_lithuanian_language': true/false}."
        },
        {"role": "user", "content": question}
    ],
    temperature=0.7
)

# Extract and validate content using Pydantic
try:
    raw_json = response.choices[0].message.content
    if raw_json is None:
        raise ValueError("Response content is None, cannot parse JSON.")
    parsed = LithuanianQuestionCheck.model_validate(json.loads(raw_json))

    if parsed.is_lithuanian_language:
        print("Puiku! Atsakau: \n")

        answer = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": "Atsakyk į klausimą lietuviškai."},
                {"role": "user", "content": question}
            ]
        )
        reply = answer.choices[0].message.content
        print("Atsakymas:", reply.strip() if reply else "(nėra atsakymo)")
    else:
        print("Klausimas nėra lietuvių kalba, todėl neatsakysiu.")

except Exception as e:
    print(f"[red]Klaida:[/red] {e}")
