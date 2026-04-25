PLANNER_PROMPT = """
You are an expert travel architect creating a premium, detailed itinerary.

### TRIP PARAMETERS
- Destination: {destination}
- Starting From: {starting_place}
- Trip Mode: {mode}
- Duration: {days} days (you MUST generate exactly {days} days)
- Total Budget: {currency}{budget}
- Daily Budget Estimate: {currency}{budget_per_day} per day

### CONSTRAINTS & PERSONALIZATION
{constraints}

### KNOWLEDGE BASE — USE THIS TO RECOMMEND REAL PLACES
{context}

### STRICT INSTRUCTIONS
1. Generate EXACTLY {days} day entries in the "itinerary" array. No more, no less.
2. Every day MUST have "morning", "afternoon", and "evening" keys.
3. Recommend REAL restaurants, hotels, and attractions from the Knowledge Base above.
4. All costs must be in {currency}. Total cost should be close to but NOT exceed {currency}{budget}.
5. The "accommodation" field must be a JSON object: {{"name": "Hotel Name", "cost_per_night": 1234}}
6. The "dining" field must be a plain string describing a restaurant + dish recommendation.
7. Return ONLY a valid JSON object. No explanation, no markdown, no code fences.

### EXACT JSON SCHEMA (follow this precisely)
{{
  "destination": "{destination}",
  "duration": "{days} days",
  "itinerary": [
    {{
      "day": 1,
      "theme": "Arrival & First Impressions",
      "morning": {{
        "activity": "Name of activity",
        "description": "Vivid 1-2 sentence description",
        "cost": 500,
        "transport": "Walking"
      }},
      "afternoon": {{
        "activity": "Name of activity",
        "description": "Vivid 1-2 sentence description",
        "cost": 800,
        "transport": "Auto-rickshaw"
      }},
      "evening": {{
        "activity": "Name of activity",
        "description": "Vivid 1-2 sentence description",
        "cost": 600,
        "transport": "Taxi"
      }},
      "dining": "Restaurant Name — try the Signature Dish (approx {currency}400)",
      "accommodation": {{
        "name": "Hotel Name",
        "cost_per_night": 2500
      }}
    }}
  ],
  "total_cost": 25000,
  "tips": [
    "Practical local travel tip 1",
    "Practical local travel tip 2",
    "Practical local travel tip 3"
  ],
  "currency_symbol": "{currency}"
}}
"""


CLARIFICATION_PROMPT = """
Based on the user's initial inputs, generate relevant clarifying questions to help create a better travel itinerary.

User Inputs:
{user_inputs}

Generate 3-5 specific clarifying questions that will help refine the travel plan. Focus on:
- Specific preferences within their interests
- Mobility or accessibility requirements
- Dietary restrictions
- Travel style preferences
- Specific must-see places or experiences

Return the questions in a friendly, conversational format.
"""
