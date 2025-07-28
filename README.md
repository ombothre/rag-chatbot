# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot specialized in answering questions about Changi Airport and Jewel Changi Airport.  
It uses LangChain, Qdrant, and Gemini for document retrieval and LLM-based responses, with a FastAPI backend and Redis for session storage.

---

## Langgraph Flow

<img width="429" height="559" alt="image" src="https://github.com/user-attachments/assets/7b5563a8-1be6-42d3-b3ad-e231400dd5a0" />

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
│   │   └── tools.py        # tools for agent 
│   └── main.py             # Entrypoint for agent logic
│
├── backend/                # FastAPI backend
│   ├── config/             # Backend settings
│   ├── helpers/            # Message serialization helpers
│   ├── models/             # API request/response models
│   ├── services/           # Lifespan and Redis client
│   └── main.py             # API endpoints
│
├── rag.py                  # CLI entrypoint for chatting
├── api.py                  # Run FastAPI server with Uvicorn
├── Dockerfile              # Docker build instructions
├── docker-compose.yml      # Multi-container orchestration
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
    REDIS_URL=localhost
    REDIS_PORT=6379
    ```

4. **Prepare data**

    - Place your PDFs and text files in the appropriate `agent/services/scraper/data/...` folders.

---

## Usage

### 1. Run the API server (locally)

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

---

## Docker Compose

A `docker-compose.yml` is provided for running both the app and Redis together.
```

### Start all services

```bash
docker compose up --build
```

- The FastAPI app will be available at [http://localhost:8000/docs](http://localhost:8000/docs).
- Redis will be available internally as `redis:6379`.

---

## Redis

- The backend uses Redis for storing chat session history.
- Redis connection details are configured via environment variables (`REDIS_URL`, `REDIS_PORT`).
- On startup, the backend connects to Redis and stores the connection in `app.state.redis_db`.
- If Redis is unavailable, API endpoints will return a 503 error.

---

## Notes

- The project uses `uv` for dependency management (`pyproject.toml` and `uv.lock`).
- Make sure your `.env` file is available and passed to the container using `--env-file` or via Docker Compose.
- For local development, ensure Redis is running (`docker run -p 6379:6379 redis:7` or use Docker Compose).

---

