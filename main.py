import os

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from groq import Groq

load_dotenv()

# CONSTANTS & VARIABLES
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
KNOWLEDGE_FILE = "sample.docs/knowledge.txt"

# FASTAPI APP
app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# BASIC CHAT
def basic_chat(question):
    client = Groq(api_key=API_KEY)

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
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


# HOME PAGE
@app.get("/")
def home(request: Request, mode: str = "basic"):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"answer": None, "question": "", "mode": mode},
    )


# CHAT ENDPOINT
@app.post("/chat")
def chat(
    request: Request, question: str = Form(...), mode: str = Form(...)
):
    if mode == "rag":
        answer = rag_chat(question)
    else:
        answer = basic_chat(question)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"answer": answer, "question": question, "mode": mode},
    )