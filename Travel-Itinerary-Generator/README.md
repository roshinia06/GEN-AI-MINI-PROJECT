# 🌍 TRAVEL ITINERARY PLANNER . AI — Travel Itinerary Generator

An AI-powered travel planning system that generates rich, personalized multi-day itineraries using a **6-agent LangGraph workflow** with real-world data from Booking.com, Geoapify, and Wikipedia.

---

## 🏗️ Project Structure

```
Travel-Itinerary-Generator/
├── backend/
│   └── main.py              # FastAPI server — REST API endpoints
├── agents/
│   ├── mode_agent.py        # Trip mode logic (seasonal/short_trip/surprise)
│   ├── retrieval_agent.py   # Gathers context from all data sources
│   ├── planner_agent.py     # LLM itinerary generation
│   ├── budget_agent.py      # Budget enforcement & breakdown
│   ├── validator_agent.py   # Schema & day-count validation
│   └── formatter_agent.py   # Final output normalization
├── graph/
│   └── workflow.py          # LangGraph StateGraph definition
├── rag/
│   ├── wiki_loader.py       # Wikipedia knowledge fetcher
│   ├── geoapify_loader.py   # Points-of-interest via Geoapify
│   ├── booking_loader.py    # Real hotel data via Booking.com API
│   ├── flight_loader.py     # Flight estimates via Booking.com API
│   ├── food_loader.py       # Food suggestions via Sharanz API
│   ├── vector_store.py      # ChromaDB vector store
│   ├── processor.py         # Text pre-processing
│   └── ingest.py            # CSV dataset ingestion script
├── utils/
│   ├── prompt_templates.py  # PLANNER_PROMPT and other LLM prompts
│   └── pdf_generator.py     # ReportLab PDF export
├── frontend/                # React UI (Create React App)
├── data/                    # CSV travel datasets
├── tests/
│   ├── test_backend.py      # FastAPI endpoint tests
│   └── test_geoapify.py     # Geoapify integration test
├── config.py                # Env var loader
├── TECHNICAL_DOCUMENTATION.md # Detailed handover guide for developers
├── requirements.txt         # Python dependencies
└── .env                     # API keys (not committed)
```

---

---

## 🤖 Detailed AI Workflow (LangGraph)

The application uses an advanced **Multi-Agent Orchestration** system powered by **LangGraph**. Instead of a single prompt, your request is processed by a pipeline of specialized agents, each refining the plan until it reaches agency-grade quality.

### 🔄 The Generation Pipeline

1.  **Mode Agent (`mode_agent.py`)**:
    - **Purpose**: Interprets the user's "Trip Persona".
    - **Logic**: If you pick **Seasonal**, it detects the current month/season and adds curated constraints. If you pick **Surprise**, it selects a hidden gem. It builds the primary instruction set for the LLM.

2.  **Retrieval Agent (`retrieval_agent.py`)**:
    - **Purpose**: Enriches the request with real-world knowledge.
    - **Data Sources**: Fetches data from **Wikipedia** (context), **Geoapify** (POI), and **ChromaDB** (Curated local insights).
    - **Optimization**: Structures raw API data into clean, searchable context strings for the AI.

3.  **Planner Agent (`planner_agent.py`)**:
    - **Purpose**: The "Architect" of the trip.
    - **Logic**: Generates **3 distinct options** (Budget, Standard, Premium). It uses a specialized prompt to ensure narrative transitions (e.g., *"We will proceed towards..."*) and explicit hotel/transport mentions.
    - **Model**: Powered by **Ollama (Llama3/Mistral)**.

4.  **Budget Agent (`budget_agent.py`)**:
    - **Purpose**: Financial auditor.
    - **Logic**: Calculates cost breakdowns for every generated option (Accommodation, Food, Activities, Buffer). It ensures the "Budget" option respects the user's spending limit while keeping "Premium" aspirational.

5.  **Validator Agent (`validator_agent.py`)**:
    - **Purpose**: Quality Control.
    - **Logic**: Verifies that each option has the correct number of days, valid hotel info, and at least 2 activities per day. If it detects errors, it flags them for the formatter to handle.

6.  **Formatter Agent (`formatter_agent.py`)**:
    - **Purpose**: Final Data Normalization.
    - **Logic**: Cleans up the AI response, ensures the JSON matches the frontend schema perfectly, and prepares the data for the **ReportLab PDF generator**.

### 📦 State Management
The entire process is governed by a `WorkflowState` object in **LangGraph**. This state acts as a "shared memory" that allows agents to see what previous agents have done, ensuring a cohesive and non-hallucinatory itinerary.

---

## ⚙️ Setup

### 1. Install Dependencies

```bash
# From the project root (Travel-Itinerary-Generator/)
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Configure Environment

Edit the `.env` file in the root directory:
```env
MODEL_NAME=llama3.2
GEOAPIFY_API_KEY=your_geoapify_key
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=booking-com.p.rapidapi.com
```

### 3. Pull the AI Model

```bash
ollama pull llama3.2
```

---

## 🚀 Running the App

> ⚠️ **Both commands must be run from the `Travel-Itinerary-Generator/` root directory.**

**Start the Backend:**
```bash
# From Travel-Itinerary-Generator/
python -m uvicorn backend.main:app --reload
```

**Start the Frontend (in a new terminal):**
```bash
# From Travel-Itinerary-Generator/
cd frontend
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🗺️ Trip Modes

| Mode | Description |
|------|-------------|
| 🌤️ **Seasonal** | Relaxed plan optimized for the current season & month |
| ⚡ **Short Trip** | High-efficiency "Power Trip" — maximum sights, minimal time |
| 🎁 **Surprise Me** | AI picks a hidden-gem destination you won't know until you open it |

---

## 🧪 Running Tests

```bash
# From Travel-Itinerary-Generator/
pytest tests/ -v
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/generate-itinerary` | Generate full itinerary |
| POST | `/api/generate-pdf` | Generate downloadable PDF |
| POST | `/api/chat` | Chat with AI about the itinerary |
| GET | `/api/destinations` | Popular destination suggestions |

### Sample Request

```json
POST /api/generate-itinerary
{
  "destination": "Paris",
  "budget": "1000 USD",
  "days": 5,
  "mode": "seasonal",
  "starting_place": "London",
  "people_count": 2,
  "interests": ["culture", "food", "art"],
  "accommodation_type": "Mid-range",
  "notes": "Vegetarian food preferred"
}
```

---

## 🔑 API Keys Used

| Service | Purpose |
|---------|---------|
| [Geoapify](https://www.geoapify.com/) | Points of interest & geocoding |
| [RapidAPI — Booking.com](https://rapidapi.com/tipsters/api/booking-com) | Real hotel data |
| [RapidAPI — Booking.com v15](https://rapidapi.com/DataCrawler/api/booking-com15) | Flight estimates |
| [RapidAPI — Sharanz](https://rapidapi.com/sharanz/api/sharanz-restraunt-api) | Food recommendations |
