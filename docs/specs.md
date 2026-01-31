# Hypemeter Technical Specification v1.0

## 1. Project Overview
**Hypemeter** is a minimalist web application that quantifies the "hype level" of any user-defined topic. By synthesizing data from search intent, social conversation, and media coverage, the app provides an objective score of a topic's cultural or technical relevance.

---

## 2. Core Functional Requirements

### 2.1 User Interface (UI)
* **Search-First Experience:** A clean, centered search bar (similar to Google) on the landing page.
* **Processing State:** A "Busy/Analyzing" animation triggered upon submission of a new or expired keyword.
* **Result View:**
    * **Primary Score:** Large numerical Hype Score (0–100).
    * **Status Label:** Dynamic text based on score (Viral, Dead Zone, or Neutral).
    * **7-Day Pulse:** A line graph showing the score's movement over the last week.
    * **Contextual Comparison:** Automatic overlay of 2–3 related high-performing topics for scale.

### 2.2 Scoring Logic & Benchmarking
The **Total Hype Score ($S$)** is a weighted average of three data streams, normalized against the highest-performing "viral" topics currently on the web.

* **Weighting Distribution:**
    1.  **Google Trends (50%):** Measures active search intent.
    2.  **Bluesky (30%):** Measures real-time social chatter and velocity.
    3.  **News Headlines (20%):** Measures media authority and narrative.

* **Status Thresholds:**
    * **Score $\ge$ 90:** "VIRAL"
    * **Score 50 – 89:** "NEUTRAL / TRENDING"
    * **Score $<$ 50:** "DEAD ZONE"

---

## 3. Technical Architecture

### 3.1 Platform & Stack
* **Type:** Responsive Web Application using full-stack framework (Django).
* **Database:** Redis or PostgreSQL for caching.
* **Frontend:** Use HTMX for adding interactivity, no heavy fornt-end framewoks.

### 3.2 Data Handling & Caching
To manage API costs and ensure performance for a free tool:
* **TTL (Time-To-Live):** 24-hour cache for all keyword results.
* **Sequence:**
    1.  Check DB for keyword.
    2.  If exists AND < 24h old: Serve cached data instantly.
    3.  If not: Trigger API fetch, calculate score, update DB, and serve.



---

## 4. Error Handling Strategies

| Error Type | Scenario | Expected Mitigation |
| :--- | :--- | :--- |
| **API Rate Limit** | Too many requests to Google/Bluesky. | Serve stale cache data (if available) or display "Server overloaded, try again later." |
| **Zero Data** | Obscure/Niche keyword with no hits. | Display: "Not enough data to calculate hype. Try a broader term." |
| **Timeout** | API takes >10 seconds to respond. | Frontend displays a "Timeout" message with a manual "Retry" button. |
| **Malformed Input** | Special characters or empty strings. | Sanitization on the frontend to prevent invalid API queries. |

---

## 5. Testing Plan

### 5.1 Backend Logic Tests
* **Normalization Test:** Ensure that even if one source (e.g., News) has 0 hits, the formula still outputs a score relative to the other weighted sources.
* **Cache Invalidation:** Verify that at hour 25, the system successfully purges old data and fetches fresh API results.

### 5.2 Frontend & UI Tests
* **Responsiveness:** Test on iOS/Android mobile browsers to ensure the 7-day graph is readable.
* **State Management:** Ensure the "Busy" animation is correctly dismissed only after all three data streams have returned a status.

### 5.3 Data Integrity
* **Comparison Logic:** Verify the "Automatic Comparison" successfully identifies relevant peers (e.g., searching "Ethereum" should trigger "Bitcoin" as a comparison).

---

## 6. Deployment Notes
* **Environment Variables:** Securely store API keys for News aggregators and Bluesky login credentials.
* **Rate Limiting:** Implement IP-based rate limiting on the search bar to prevent bot abuse of the free API calls.