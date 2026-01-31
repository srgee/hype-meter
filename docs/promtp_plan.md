# Hypemeter: Development Blueprint & Prompt Guide

## 1. Architectural Strategy
To meet the requirements for robust data analysis (`pytrends`) and a reactive, modern UI, we will use a **Split Stack Architecture**:

* **Backend:** **Python (FastAPI)**. Python is non-negotiable for the data science libraries (`pytrends`, `pandas`). FastAPI provides high performance and easy async handling for parallel API requests.
* **Frontend:** **Next.js (React)**. Ensures a fast, responsive Single Page Application (SPA) experience with excellent libraries for visualization (`recharts`).
* **Database/Cache:** **Redis**. Essential for the 24-hour TTL (Time-To-Live) caching requirement to minimize API costs.

---

## 2. The Iterative Execution Plan
We will build this in 4 distinct phases to ensure stability before adding complexity.

1.  **Phase 1: The Backend Core (Infrastructure)**
    * Set up FastAPI.
    * Connect Redis.
    * Establish the project structure.
2.  **Phase 2: Data Pipelines (The "Senses")**
    * Build the Google Trends fetcher.
    * Build the Bluesky (Social) fetcher.
    * Build the NewsAPI fetcher.
3.  **Phase 3: The Brain (Logic & Caching)**
    * Implement the weighted scoring algorithm.
    * Implement the normalization logic (0-100 scale).
    * Wire up the 24-hour caching layer.
4.  **Phase 4: The Face (Frontend & Viz)**
    * Build the Next.js search UI.
    * Connect to the Backend.
    * Render the Hype Graph.

---

## 3. LLM Prompts (Copy & Paste these sequentially)

### Phase 1: Backend Infrastructure

**Prompt 1: Project Setup & Redis**
```text
Act as a Senior Backend Python Developer. We are building "Hypemeter," an app that calculates internet hype for specific keywords.

We will use FastAPI for the backend and Redis for caching.

Please initialize a new FastAPI project structure. 
1. Create a `main.py` entry point.
2. Create a `config.py` to handle environment variables (REDIS_URL, API_KEYS).
3. Create a `database.py` file that initializes an asynchronous Redis client (`redis-py` or `aioredis`).
4. Write a dependency function `get_cache` to easily access Redis in our routes.
5. Create a simple health check endpoint `GET /health` that returns `{"status": "ok", "redis": "connected"}` (verify the Redis connection works).

Use Pydantic for settings management. Ensure error handling if Redis is not reachable.