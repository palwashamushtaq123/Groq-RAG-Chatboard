import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from groq import Groq


load_dotenv()

# CONSTANTS & VARIABLES
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
KNOWLEDGE_FILE = "sample_docs/knowledge.txt"


# FASTAPI APP
app = FastAPI(title="Groq AI Chat")


# STATIC FILES
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# GROQ CLIENT
client = Groq(api_key=API_KEY)


# REQUEST MODEL
class ChatRequest(BaseModel):
    message: str
    mode: str = "basic"
    history: list = []


# HOME PAGE
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# CHAT API
@app.post("/chat")
async def chat(data: ChatRequest):

    if not data.message.strip():
        return {
            "reply": "Please enter a message."
        }

    # BASIC CHAT
    if data.mode == "basic":

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]

        # Add previous conversation
        messages.extend(data.history)

        # Add current user message
        messages.append({
            "role": "user",
            "content": data.message
        })

        response = client.chat.completions.create(
            messages=messages,
            model=MODEL
        )

        reply = response.choices[0].message.content

        return {
            "reply": reply
        }

    # RAG CHAT
    elif data.mode == "rag":

        try:
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
                document = file.read()

        except FileNotFoundError:
            return {
                "reply": "Knowledge file was not found."
            }

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful RAG assistant. "
                        "Answer the user's question using only "
                        "the provided document. "
                        "If the answer is not present in the document, "
                        "say that the information is not available "
                        "in the knowledge document."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Document:\n\n{document}\n\n"
                        f"Question:\n{data.message}"
                    )
                }
            ],
            model=MODEL
        )

        reply = response.choices[0].message.content

        return {
            "reply": reply
        }

    else:
        return {
            "reply": "Invalid chat mode."
        }