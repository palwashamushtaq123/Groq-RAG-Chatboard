# ✦ RAG Chatboard - AI Knowledge Assistant

An end-to-end full-stack AI Assistant application built with a **FastAPI** backend integrated with **Groq Cloud API** (`llama-3.3` / `gpt-oss-20b`), utilizing a **Retrieval-Augmented Generation (RAG)** engine for contextual document querying.

---

## 🌐 Live Demos & Architecture

The application follows a decoupled multi-cloud architecture:

* **🎨 Frontend UI (Firebase Hosting):** [https://rag-chatboard.web.app](https://rag-chatboard.web.app)  
  *Built using HTML, CSS, and modern asynchronous JavaScript.*
* **⚡ Backend API (Vercel):** [https://rag-chatboard.vercel.app](https://rag-chatboard.vercel.app)  
  *Built with FastAPI, powering both basic conversational AI and document RAG processing.*

---

## 🌟 Key Features

* **💬 Basic Chat Mode**: Fast, general-purpose AI conversation powered by Groq API.
* **📚 RAG Chat Mode**: Context-aware answering using custom knowledge base files (`sample.docs/knowledge.txt`).
* **⚡ High-Performance FastAPI**: Asynchronous REST API with CORS enabled for seamless web access.
* **💻 Dual Interfaces**: Supports both a modern web UI and an interactive Terminal/CLI mode.
* **🐳 Docker Support**: Fully containerized setup ready for container-based cloud platforms.

---

## 📁 Project Structure & Git Tracking Guide

Below is the directory structure indicating which files are tracked by Git and which are ignored via `.gitignore`:

```text
Rag chatboard/
├── public/
│   └── index.html            # [GIT TRACKED] Frontend Web Interface (Firebase Hosting)
├── static/
│   └── style.css             # [GIT TRACKED] CSS Styling for UI
├── sample.docs/
│   └── knowledge.txt         # [GIT TRACKED] Knowledge base context document for RAG
├── .env                      # [GIT IGNORED] Private environment variables & API keys
├── .env.example              # [GIT TRACKED] Template for environment variables
├── .firebase/                # [GIT IGNORED] Local Firebase CLI build cache
├── .firebaserc               # [GIT TRACKED] Firebase project association config
├── .gitignore                # [GIT TRACKED] Git ignore configuration
├── .vercel/                  # [GIT IGNORED] Local Vercel deployment cache
├── __pycache__/              # [GIT IGNORED] Compiled Python bytecode files
├── Dockerfile                # [GIT TRACKED] Docker container runtime configuration
├── firebase.json             # [GIT TRACKED] Firebase hosting routing & public directory config
├── main.py                   # [GIT TRACKED] FastAPI web server application
├── main_terminal_code.py     # [GIT TRACKED] Interactive terminal/CLI script
├── requirements.txt          # [GIT TRACKED] Python dependency package list
├── venv/                     # [GIT IGNORED] Local Python virtual environment
└── vercel.json               # [GIT TRACKED] Vercel serverless deployment config
```

---

## 🛡️ Recommended `.gitignore` Setup

Ensure your local `.gitignore` file contains the following rules:

```gitignore
# Virtual Environments
venv/
.venv/
env/

# Secrets & Environment Variables
.env
.env.local

# Python Cache
__pycache__/
*.py[cod]

# IDE / Editor Folders
.vscode/
.idea/

# Deployment Caches
.firebase/
.vercel/
*.log
```

---

## 🛠️ Step-by-Step Setup & Local Development

### 1. Clone & Setup Repository
```bash
git clone https://github.com/your-username/rag-chatboard.git
cd rag-chatboard
```

### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root directory and insert your Groq API credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

---

## 🚀 How to Run Locally

### Option A: Local Web Server (FastAPI Backend)
Run the backend server using Uvicorn:
```bash
uvicorn main:app --reload --port 8000
```
* Access the health check endpoint at `http://127.0.0.1:8000/`.
* Open `public/index.html` in your browser or serve it via local web server.

### Option B: Terminal / CLI Mode
Run the interactive command-line interface directly:
```bash
python main_terminal_code.py
```

### Option C: Docker Container
Build and execute the project within a Docker container:
```bash
# Build Docker image
docker build -t rag-chatboard .

# Run Docker container
docker run -p 8080:8080 --env-file .env rag-chatboard
```

---

## 📡 API Endpoints Reference

### `GET /`
* **Description**: Health check endpoint verifying backend status.
* **Response**:
  ```json
  {
    "status": "online",
    "message": "RAG Chatboard API is running"
  }
  ```

### `POST /chat`
* **Description**: Primary chat endpoint processing both basic AI prompts and RAG queries.
* **Form Parameters**:
  * `question` *(string, required)*: The user's prompt or question.
  * `mode` *(string, required)*: Chat mode (`basic` or `rag`).
* **Response Example**:
  ```json
  {
    "success": true,
    "answer": "Generated answer based on knowledge document...",
    "question": "What is in the knowledge base?",
    "mode": "rag"
  }
  ```s