import openai
import os

from dotenv import load_dotenv
from rich import print

load_dotenv()  # Load environment variables from .env file

token = os.getenv("SECRET")  # Replace with your actual token
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

# Complaint letter recogniser

# Generate me a mock complaint letter
complaint_letter = """Dear Customer Service,
I am writing to express my dissatisfaction with the recent purchase I made from your store.
 The product arrived damaged and did not match the description provided on your website. 
 I expected a much higher quality based on the price I paid. I would like a full refund and an apology for the inconvenience caused.
Thank you for your attention to this matter.
Sincerely,"""

love_letter = """ I love you more than words can express."""

# Initialize the OpenAI client
client = openai.OpenAI(
    api_key=token,
    base_url=endpoint)

response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": """You are a helpful assistant that recognises complaint letters. 
             Please let us know if the letter is a complaint or not? Please response with True or False."""},
            {"role": "user", "content": complaint_letter}
        ],
        temperature=0.7
    )

print(response.choices[0].message.content)

text = response.choices[0].message.content
if "true" in text.lower():
    print("[bold red]This is a complaint letter.[/bold red]")
else:
    print("[bold green]This is not a complaint letter.[/bold green]")