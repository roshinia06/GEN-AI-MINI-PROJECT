# Wanderer AI: Production-Grade Travel Planner

A premium, multi-agent travel orchestration system powered by **LangGraph**, **Ollama (Llama 3.2)**, and a **Hybrid RAG** engine. Wanderer AI generates stunning, real-world itineraries with live data from Wikipedia, Geoapify, Booking.com, and more.

## 🏗️ Advanced Multi-Agent Architecture

The system uses a sophisticated 6-agent pipeline to ensure accuracy, feasibility, and style:

```text
User Input → [Mode Agent] → [Retrieval Agent] → [Planner Agent] → [Budget Agent] → [Validator Agent] → [Formatter Agent] → UI/PDF
```

### 🤖 The Agent Team
- **Mode Agent**: Detects the trip "persona" (Seasonal, Power Trip, or Surprise Me) and sets strategic constraints.
- **Retrieval Agent**: Orchestrates data from Wikipedia, Geoapify, Booking.com, and Flight APIs.
- **Planner Agent**: Crafts the day-by-day narrative using context-aware Llama 3.2 logic.
- **Budget Agent**: Intelligently swaps components (like hotels) to stay within financial limits.
- **Validator Agent**: Ensures the plan is complete, logically sound, and satisfies all user notes.
- **Formatter Agent**: Normalizes outputs for the React UI and high-end PDF engine.

## 🌟 Key Features

- **🎯 Specialized Trip Modes**:
  - **Seasonal Vacation**: Automatically detects current season (e.g., Spring) for time-appropriate activities.
  - **Power Trip**: High-efficiency, fast-paced logistics for 1-3 day "must-see" sprints.
  - **Surprise Me**: Autonomous destination selection and "hidden gem" discovery.
- **🌐 Real-World Data Integration**:
  - **Wikipedia**: Historical and cultural context.
  - **Geoapify**: Attraction names and geolocation.
  - **Booking.com (RapidAPI)**: Live hotel options with real ratings and prices.
  - **Flights (RapidAPI)**: Indicative pricing based on origin-destination city pairs.
  - **Restaurant API**: Tailored veg/non-veg dish suggestions.
- **💬 Chat Concierge**: An interactive LLM-based concierge that "knows" your itinerary and can answer questions or suggest refinements.
- **📄 Premium PDF Export**: Download beautiful, structured itineraries with professional layout and budget breakdowns.
- **🛠️ Production Ready**: Migrated to Pydantic V2 for robust validation and clean FastAPI endpoints.

## 🚀 Setup Instructions

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Ollama** (with `llama3.2` model installed)

### 1. Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Frontend dependencies
cd frontend
npm install
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
MODEL_NAME=llama3.2
GEOAPIFY_API_KEY=your_key
RAPIDAPI_KEY=your_key
RAPIDAPI_HOST=booking-com.p.rapidapi.com
```

### 3. Running the App
1. **Start the Backend**:
   ```bash
   cd backend
   python main.py
   ```
2. **Start the Frontend**:
   ```bash
   cd frontend
   npm start
   ```

## 📂 Project Structure

```text
├── agents/                 # AI Expert logic (Mode, Planner, Budget, etc.)
├── backend/                # FastAPI REST API & PDF Endpoints
├── frontend/               # ReactJS Modern UI (Tabs, Chat, Forms)
├── graph/                  # LangGraph Workflow definitions
├── rag/                    # Data Loaders (Wiki, Booking, Flights, Food)
├── utils/                  # Prompt Templates & PDF Generator
├── config.py               # Central configuration management
└── requirements.txt        # Backend dependencies
```

## 🤝 Technology Stack
- **AI Framework**: LangGraph, Ollama, LangChain
- **Backend**: FastAPI, Pydantic V2, ReportLab
- **Frontend**: React, Lucide Icons, Custom CSS3
- **Data**: Wikipedia, Geoapify, RapidAPI (Booking.com & Flights)

---
*Built with ❤️ for modern travelers.*
