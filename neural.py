import os
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_ai_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Ты — дружелюбный карьерный помощник."},
                  {"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
