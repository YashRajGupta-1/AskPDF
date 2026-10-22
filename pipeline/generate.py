import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads GROQ_API_KEY from .env
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"

SYSTEM = ("Answer using ONLY the context below. "
          "If the answer is not there, say exactly: I don't know. "
          "Cite facts like [1], [2].")

def build_prompt(question, chunks):
    ctx = "\n\n".join(
        f"[{i+1}] (page {c['page']}) {c['text']}"
        for i, c in enumerate(chunks))
    return f"{SYSTEM}\n\nCONTEXT:\n{ctx}\n\nQUESTION: {question}\nANSWER:"

def ask_llm(prompt):
    r = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": prompt}],
              "temperature": 0.1},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]