# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot specialized in answering questions about Changi Airport and Jewel Changi Airport.  
It uses LangChain, Qdrant, and Gemini for document retrieval and LLM-based responses, with a FastAPI backend.

---

## Project Structure

```
rag-chatbot/
│
├── agent/                  # Core AI logic and RAG pipeline
│   ├── ai/                 # LLM, prompts, graph logic
│   ├── config/             # Settings and secrets
│   ├── models/             # State and node definitions
│   ├── services/           # RAG, vector DB, helpers, scraping
│   │   │── tools.py        # tools for agent 
│   └── main.py             # Entrypoint for agent logic
│
├── backend/                # FastAPI backend
│   ├── models/             # API request/response models
│   └── main.py             # API endpoints
│
├── rag.py                  # CLI entrypoint for chatting
├── api.py                  # Run FastAPI server with Uvicorn
├── Dockerfile              # Docker build instructions
└── README.md
```

---

## Setup

1. **Clone the repository**

    ```bash
    git clone <repo-url>
    cd rag-chatbot
    ```

2. **Install dependencies**

    ```bash
    pip install uv
    uv sync
    ```

3. **Set environment variables**

    Create a `.env` file in `agent/config/` with:

    ```
    GEMINI_API_KEY=your_gemini_api_key
    QDRANT_URL=your_qdrant_url
    QDRANT_API_KEY=your_qdrant_api_key
    ```

4. **Prepare data**

    - Place your PDFs and text files in the appropriate `agent/services/scraper/data/...` folders.

---

## Usage

### 1. Run the API server

```bash
python api.py
```

- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs.

#### Example API call

```http
POST /api/ask
{
  "question": "What are the amenities at Jewel Changi Airport?"
}
```

### 2. Chat via CLI

```bash
python rag.py
```

---

## Docker

You can run the chatbot using Docker for easy deployment.

### Build the Docker image

```bash
docker build -t rag-chatbot .
```

### Run the Docker container

```bash
docker run -p 8000:8000 --env-file agent/config/.env rag-chatbot
```

- The API will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

**Note:**  
- Make sure your `.env` file is available and passed to the container using `--env-file`.
- The provided `Dockerfile` uses `uv` for dependency management and expects your dependencies to be defined in `pyproject.toml