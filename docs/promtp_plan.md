# Hypemeter: Master Development Blueprint & LLM Prompts

__Version:__ 1.0 
__Stack:__ Django 6.0, Python 3.13+, uv, HTMX, TailwindCSS, Pydantic.

# Part 1: Technical Specification
## 1. Project Overview

Hypemeter is a minimalist web application that quantifies the "hype level" of any user-defined topic. By synthesizing data from search intent, social conversation, and media coverage, the app provides an objective score of a topic's cultural or technical relevance.

## 2. Core Functional Requirements

- Search-First Experience: Google-like clean search bar using HTMX.
- Scoring Logic: Weighted average (50% Google Trends, 30% Social, 20% News).
- Visualization: 7-Day pulse graph using Chart.js.
- Performance: "Cache-first" architecture (24h TTL) to minimize API calls.

## 3. Implementation Strategy (The "Steel Thread")

We will build this in 5 distinct phases to ensure stability:

1. Foundation: Project setup with modern 2026 standards (uv, apps/ folder). Project boilerplate is doen manually.
2. The Core (Mocked): Database models and a service layer returning fake data to test the flow.
3. The UI: HTMX frontend to display the fake data.
4. The Flesh: Replacing fake data with real APIs (Trends, News, Social) one by one.
5. The Polish: Adding the Chart.js visualization and error handling.

# Part 2: Implementation Prompts for LLM

Copy and paste these prompts one by one into your AI Code Assistant (Claude 3.5, GPT-4o, etc.). Do not proceed to the next prompt until the previous step is working.

## Prompt 01: Data Model & Service Layer (Mock Strategy)

Goal: Create the database schema and the logic engine (using fake data first)

We have a working Django shell. Now, let's build the Domain Model and the Service Layer.

1.  **The Model (`apps/core/models.py`):**
    - Create a model named `Topic`.
    - Fields:
        - `name`: CharField (unique, indexed).
        - `score`: IntegerField (0-100).
        - `status_label`: CharField (choices: VIRAL, NEUTRAL, DEAD).
        - `history_data`: JSONField (stores the last 7 days of scores for the graph).
        - `last_updated`: DateTimeField (auto_now=True).
    - Add a method `is_stale()` that returns `True` if `last_updated` is older than 24 hours.

2.  **The Service Layer (`apps/core/services.py`):**
    - Create a class `HypeEngine`.
    - Add a method `get_hype(topic_name: str) -> Topic`.
    - **Logic:**
        - Check if the topic exists in the DB.
        - If it exists AND `is_stale()` is False, return the DB object.
        - If it does not exist OR `is_stale()` is True, call `self._calculate_score(topic_name)`.
    
3.  **Mock Implementation:**
    - Implement `_calculate_score` to strictly return MOCK data for now (we will add APIs later).
    - Generate a random integer (0-100).
    - Generate a random list of 7 integers for `history_data`.
    - Determine `status_label`: >=90 "VIRAL", 50-89 "NEUTRAL", <50 "DEAD".
    - Save/Update the `Topic` in the DB and return it.

4.  **Management Command:**
    - Create a management command `python manage.py check_topic <name>` that calls this service and prints the result, so I can test it in the terminal.

## Prompt 02: HTMX Search Interface

Goal: Build the frontend interaction.

Now let's build the UI using Django Templates and HTMX.

1.  **Base Template:**
    - Create `templates/base.html` using Tailwind CSS (via CDN script).
    - Include the HTMX library (via CDN script).
    - Add a clean, dark-mode styling structure.

2.  **Search View (`apps/core/views.py`):**
    - Create a view `index` that renders the landing page.
    - The landing page should have a centered, large Search Bar.
    - The form should use HTMX:
        - `hx-post="{url 'search'}"`
        - `hx-target="#result-container"`
        - `hx-indicator="#loading-spinner"`
        - `hx-swap="innerHTML"`

3.  **Search Logic:**
    - Create a view `search_topic` that accepts the POST request.
    - It should instantiate `HypeEngine` and call `get_hype(query)`.
    - It should return a *partial* template (`partials/result.html`) with the topic data.

4.  **Partials:**
    - Create `templates/partials/result.html`.
    - Display the Score (Large font).
    - Display the Status Label (Color coded: Red for Viral, Gray for Dead).
    - Display the `history_data` (Just print the list of numbers as text for now, we will graph it later).

5.  **Loading State:**
    - Add a "Searching the cosmos..." spinner/div that is hidden by default and shown only when HTMX is requesting.

Ensure all URLs are wired up.

## Prompt 03: Real Data - Google Trends (50% Weight)

Goal: Replace the first chunk of fake data with real API data.

It is time to replace the Mock data with real API data. We will start with the Google Trends integration.

1.  **Dependencies:**
    - Add `pytrends` and `pandas` to the project requirements.

2.  **Trends Service (`apps/core/services/trends.py`):**
    - Create a class `TrendsProvider`.
    - Implement a method `get_interest(keyword) -> int`.
    - Use `TrendReq` to fetch data for the keyword for the timeframe 'now 7-d'.
    - **Normalization:** Take the mean value of the interest over the last 7 days and normalize it to a 0-100 scale. 
    - **Error Handling:** Wrap in try/except. If the API fails or returns no data, return 0.

3.  **Engine Integration:**
    - Update `apps/core/services.py`.
    - In `_calculate_score`, replace the random number generator for the "Search" component with this new `TrendsProvider`.
    - Update the final score formula: `Final Score = (TrendsScore * 0.5) + (Random * 0.5)` (We still keep the other 50% random until the next steps).

## Prompt 04: Real Data - News & Social (Remaining 50%)

Goal: Complete the scoring engine.

Let's complete the Scoring Engine by adding News and Social data.

1.  **News Service (`apps/core/services/news.py`):**
    - Use `httpx` (async client) to fetch data from NewsAPI (v2/everything).
    - Method: `get_media_hype(keyword) -> int`.
    - Logic: Count total results in the last 7 days.
    - Normalization: If count > 100, score is 100. Else, `count`. (Simple cap).
    - Handle missing API Key gracefully (return 0).

2.  **Social Service (`apps/core/services/social.py`):**
    - Create a `SocialProvider`.
    - Method: `get_social_velocity(keyword) -> int`.
    - **Logic:** Generate a detailed deterministic score based on a hash of the keyword (to simulate consistency without requiring a Bluesky Auth integration for this MVP). If you have a public endpoint, use it, otherwise simulate "Velocity" based on string characteristics to mimic API response.

3.  **Final Assembly (`HypeEngine`):**
    - Update `_calculate_score` to use `asyncio` to fetch Trends, News, and Social in parallel.
    - **Final Formula:** `Total = (Trends * 0.5) + (Social * 0.3) + (News * 0.2)`.
    - Update the `history_data`: Store the individual breakdown `{'trends': X, 'social': Y, 'news': Z}`.

## Prompt 05: Visualization & Polish

Goal: Add the Chart.js graph and final styles.

The backend is complete. Now let's polish the Frontend `result.html` partial.

1.  **Chart Integration:**
    - Include `Chart.js` via CDN in `base.html`.
    - In `templates/partials/result.html`, add a `<canvas id="hypeChart">`.

2.  **Data Rendering:**
    - Update the template to accept the `history_data` from the context.
    - Add a small inline `<script>` tag inside the partial that initializes the Chart.
    - **Important:** Since this is an HTMX swap, ensure the script runs after the content is loaded.

3.  **Visuals:**
    - Render a Line Chart showing the "Pulse".
    - If we don't have real 7-day history yet, render a flat line or a simulated curve based on the current score.

4.  **Status Badges:**
    - Ensure the "Viral", "Neutral", "Dead" labels have distinct Tailwind classes (e.g., `bg-red-500` vs `bg-gray-500`).