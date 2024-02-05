import os
from typing import Union
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

"""
1. When user sends a question to the server, we need to clean up the question based on NLTK or Spacy.
2. Then we send to the GPT-3 model to get the answer.
"""


class Question(BaseModel):
    question: str
    email: str


@app.post("/api/v1/ask")
def ask_question(question: Question):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question.question},
        ],
    )
    print(completion.choices[0].message)
    return completion.choices[0].message
