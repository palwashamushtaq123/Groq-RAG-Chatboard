import os

from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

load_dotenv()

# CONSTANTS
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
KNOWLEDGE_FILE = "sample.docs/knowledge.txt"

# FASTAPI APP
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# BASIC CHAT
def basic_chat(question):
    client = Groq(api_key=API_KEY)

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": question
            },
        ],
        model=MODEL,
    )

    return response.choices[0].message.content


# RAG CHAT
def rag_chat(question):
    client = Groq(api_key=API_KEY)

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        document = file.read()

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Answer using only the document below.",
            },
            {
                "role": "user",
                "content": f"Document:\n{document}\n\nQuestion: {question}",
            },
        ],
        model=MODEL,
    )

    return response.choices[0].message.content


# HEALTH CHECK
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "RAG Chatboard API is running"
    }


# CHAT ENDPOINT
@app.post("/chat")
def chat(
    question: str = Form(...),
    mode: str = Form(...)
):
    question = question.strip()

    if not question:
        return {
            "success": False,
            "error": "Please enter a question."
        }

    try:
        if mode == "rag":
            answer = rag_chat(question)
        else:
            answer = basic_chat(question)

        return {
            "success": True,
            "answer": answer,
            "question": question,
            "mode": mode
        }

    except Exception as e:
        print(f"Chat error: {e}")

        return {
            "success": False,
            "error": str(e)
        }