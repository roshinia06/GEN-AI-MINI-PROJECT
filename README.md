#   AI Travel Itinerary Planner

## Overview
This project is a **Multi-Step Travel Itinerary Generator** built using **Ollama with Llama 3.2** and **Streamlit**. It allows users to generate a personalized, structured travel itinerary based on their preferences. The system follows a guided interaction process to refine user input and provide detailed day-by-day travel plans.

## Features
- Interactive UI for collecting travel preferences.
- AI-powered itinerary generation using local LLM.
- Automatic generation of a structured, day-by-day itinerary.
- Recommendations for attractions, activities, dining, and accommodations.
- Budget tracking and cost estimation.
- Local AI processing (no external API costs).

## Tech Stack
- **Python**
- **Streamlit** (for UI)
- **Ollama** (for local AI model hosting)
- **Llama 3.2** (AI model for itinerary generation)

## Installation
### Prerequisites
- Python 3.x installed
- **Ollama** installed and running
- Required Python libraries installed

### Setup Instructions
1. **Install Ollama:**
   ```sh
   # Download and install from https://ollama.com/
   # Or use package manager:
   # macOS: brew install ollama
   # Windows: Download installer from website
   # Linux: curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Pull Llama 3.2 Model:**
   ```sh
   ollama pull llama3.2
   ```

3. **Start Ollama Service:**
   ```sh
   ollama serve
   ```

4. **Clone the Repository:**
   ```sh
   git clone https://github.com/yourusername/travel-itinerary-generator.git
   cd travel-itinerary-generator/Travel-Itinerary-Generator
   ```

5. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   # Or manually:
   pip install streamlit ollama python-dotenv
   ```

6. **Run the Streamlit App:**
   ```sh
   streamlit run app.py
   ```

## Usage
1. Ensure Ollama is running with Llama 3.2 model installed
2. Launch the Streamlit app using `streamlit run app.py`
3. Enter your travel destination, duration, budget, interests, and accommodation preferences
4. Click "Generate Itinerary" to create your personalized travel plan
5. The system will generate a structured itinerary including:
   - Day-by-day activities (morning, afternoon, evening)
   - Cost estimates for each day
   - Dining recommendations
   - Accommodation suggestions
   - Budget breakdown
   - Travel tips

## Example Output
**User Inputs:**
```
Destination: Paris
Duration: 5 days
Budget: ₹50000
Interests: Culture, food, sightseeing
Accommodation: Mid-range
Additional Notes: First time visitor
```

**Generated Itinerary:**
```json
{
  "destination": "Paris",
  "days": [
    {
      "day": 1,
      "activities": [
        "Morning: Visit Eiffel Tower and Champ de Mars",
        "Afternoon: Louvre Museum tour",
        "Evening: Seine River cruise and dinner in Latin Quarter"
      ],
      "estimated_cost": 8000,
      "dining_recommendations": [
        "Café de Flore - Classic French café",
        "Le Comptoir du Relais - Traditional bistro"
      ],
      "accommodation_suggestion": "Hotel des Grands Boulevards"
    }
  ],
  "total_cost": 45000,
  "budget_breakdown": {
    "accommodation": 15000,
    "food": 12000,
    "activities": 13000,
    "transport": 5000
  },
  "travel_tips": [
    "Buy museum passes in advance to skip lines",
    "Learn basic French phrases for better interaction"
  ]
}
```

## Project Structure
```
Travel-Itinerary-Generator/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── agents/
│   └── planner_agent.py   # AI agent for itinerary generation
└── utils/
    └── prompt_templates.py # AI prompt templates
```

## Configuration
The application uses the following configuration (in `config.py`):
- **Model**: Llama 3.2 via Ollama
- **Ollama URL**: http://localhost:11434
- **Default Model**: llama3.2

To switch to a different model, update the `OLLAMA_MODEL` variable in `config.py`.

## Troubleshooting

### Common Issues:
1. **"Connection refused" error**
   - Ensure Ollama is running: `ollama serve`
   - Check if Ollama is installed correctly

2. **"Model not found" error**
   - Pull the required model: `ollama pull llama3.2`
   - Check available models: `ollama list`

3. **"int object is not iterable" error**
   - This has been fixed in the latest version
   - Ensure you're using the updated code

4. **Slow response times**
   - Ollama runs locally, performance depends on your hardware
   - Consider using a smaller model for faster responses

### Debug Mode:
You can test the Ollama connection by running:
```python
import ollama
response = ollama.generate(model='llama3.2', prompt='Hello')
print(response)
```



