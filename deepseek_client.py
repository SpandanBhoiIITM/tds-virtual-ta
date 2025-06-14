# deepseek_client.py
import os
import requests
from dotenv import load_dotenv
load_dotenv()


API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-prover-v2:free"
API_KEY = os.getenv("OPENROUTER_API_KEY")  # Set this first

if not API_KEY:
    raise Exception("Set OPENROUTER_API_KEY in your environment.")

def call_deepseek(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a mathematical proof assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post(API_URL, headers=headers, json=body)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"DeepSeek API error {resp.status_code}: {resp.text}")
