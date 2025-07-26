# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot specialized in answering questions about Changi Airport and Jewel Changi Airport.  
It uses LangChain, Qdrant, and Gemini for document retrieval and LLM-based responses, with a FastAPI backend.

---

## Features

- **RAG-powered answers** for airport-related queries.
- **Document ingestion** from PDFs and text files.
- **FastAPI backend** for easy integration.
- **Modular agent/AI code** for extensibility.

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
│   └── main.py             # Entrypoint for agent logic
│
├── backend/                # FastAPI backend
│   ├── models/             # API request/response models
│   └── main.py             # API endpoints
│
├── rag.py                  # CLI entrypoint for chatting
├── api.py                  # Run FastAPI server with Uvicorn
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

## Key Components

- **agent/ai/graph.py**: Orchestrates the LLM, tool use, and output nodes.
- **agent/services/rag/**: Handles document loading, splitting, vector DB, and retrieval tools.
- **backend/main.py**: FastAPI endpoints for health and chat.
- **agent/main.py**: Agent setup and chat logic for both API and CLI.

---

## Extending

- Add new tools in `agent/services/rag/tools.py`.
- Add new data sources in `agent/services/scraper/`.
- Adjust prompts in `agent/ai/prompts.py`.

---