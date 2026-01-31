# Hypemeter Development Checklist

## Phase 1: Backend Infrastructure (FastAPI & Redis)

- [x] **Project Initialization**
  - [x] Initialize Git repository (`git init`).
  - [x] Create virtual environment (`python -m venv venv`).
  - [x] Install dependencies: `fastapi`, `uvicorn`, `redis`, `pydantic-settings`, `pytrends`, `atproto`, `newsapi-python`, `httpx`.

- [ ] **Core Setup**
  - [ ] Create `backend/main.py` (FastAPI app entry point).
  - [ ] Create `backend/config.py` using Pydantic BaseSettings.
    - [ ] Define `REDIS_URL`.
    - [ ] Define `NEWS_API_KEY`.
    - [ ] Define `BLUESKY_USERNAME` & `BLUESKY_PASSWORD`.
  - [ ] Create `.env` file (add to `.gitignore`).

- [ ] **Database Connection**
  - [ ] Set up local Redis instance (Docker or local install).
  - [ ] Create `backend/database.py` with async Redis client setup.
  - [ ] Write `get_cache` dependency function.
  - [ ] **Test:** Implement `GET /health` endpoint returning Redis connection status.

## Phase 2: Data Ingestion Layers

- [ ] **Google Trends Service**
  - [ ] Create `backend/services/trends.py`.
  - [ ] Implement `fetch_google_trends(keyword)` using `pytrends`.
  - [ ] Add error handling (Rate limits/429, Empty data).
  - [ ] Normalize output (0-100 scale).
  - [ ] **Test:** specific endpoint `GET /api/test/trends/{keyword}`.

- [ ] **Bluesky Service (Social)**
  - [ ] Create `backend/services/social.py`.
  - [ ] Implement auth/session management for Bluesky.
  - [ ] Implement `fetch_bluesky_volume(keyword)` (count posts in last 7 days).
  - [ ] Apply normalization logic (e.g., 1000 posts = 100 score).
  - [ ] **Test:** specific endpoint `GET /api/test/social/{keyword}`.

- [ ] **NewsAPI Service (Media)**
  - [ ] Create `backend/services/news.py`.
  - [ ] Implement `fetch_news_volume(keyword)` using `NewsApiClient`.
  - [ ] Apply normalization logic (e.g., 50 articles = 100 score).
  - [ ] **Test:** specific endpoint `GET /api/test/news/{keyword}`.

## Phase 3: The Hype Engine & Logic

- [ ] **Scoring Algorithm**
  - [ ] Create `backend/services/engine.py`.
  - [ ] Implement `calculate_hype(keyword)`:
    - [ ] Run all 3 services in parallel using `asyncio.gather`.
    - [ ] Apply weights: Trends (50%), Social (30%), News (20%).
    - [ ] Calculate final integer score (0-100).

- [ ] **Caching Layer**
  - [ ] Implement caching logic in `engine.py` or `main.py`:
    - [ ] Check Redis for key `hype:{keyword}`.
    - [ ] If exists: Return JSON.
    - [ ] If missing: Run calculation -> Save to Redis (TTL 86400s) -> Return JSON.

- [ ] **Main API Endpoint**
  - [ ] Create `GET /api/hype/{keyword}`.
  - [ ] Define response model (Pydantic schema):
    - [ ] `score` (int)
    - [ ] `label` (Viral/Neutral/Dead)
    - [ ] `history` (List[int])
    - [ ] `breakdown` (Dict)
  - [ ] **Test:** Verify data consistency and cache hit/miss behavior.

## Phase 4: Frontend Development (Next.js)

- [ ] **Setup**
  - [ ] Initialize Next.js project (`npx create-next-app@latest`).
  - [ ] Configure Tailwind CSS.
  - [ ] Install icons (`lucide-react`) and charts (`recharts`).

- [ ] **Components**
  - [ ] Create `components/SearchInput.tsx` (Centered, minimal).
  - [ ] Create `components/HypeCard.tsx` (Score display, Label styling).
  - [ ] Create `components/HypeGraph.tsx` (Recharts LineChart implementation).
  - [ ] Create `components/Loader.tsx` ("Analyzing..." animation).

- [ ] **State & Logic**
  - [ ] Create `lib/api.ts` fetcher function.
  - [ ] Implement `page.tsx`:
    - [ ] Manage `loading`, `data`, `error` states.
    - [ ] Handle API errors (404/500).
    - [ ] Implement "Viral" vs "Dead" color coding (Red vs Gray).

## Phase 5: Polish & Deployment Prep

- [ ] **Comparisons (Bonus)**
  - [ ] Implement logic to show "Compared to: [Competitor]" on the result card.

- [ ] **Optimization**
  - [ ] specific Mobile responsiveness check (Graph readability).
  - [ ] Rate limiting on Backend (FastAPI-Limiter) to prevent abuse.

- [ ] **Final Review**
  - [ ] Run full end-to-end test (Search -> Animation -> Result).
  - [ ] Verify Redis cache expires correctly.