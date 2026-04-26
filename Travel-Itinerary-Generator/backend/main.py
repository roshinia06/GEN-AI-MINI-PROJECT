"""
FastAPI Backend for AI Travel Planner
Provides REST API endpoints for travel itinerary generation

This module implements a REST API using FastAPI that serves as the backend
for the AI Travel Planner application. It handles HTTP requests from the
ReactJS frontend and coordinates with the LangGraph workflow to generate
travel itineraries.

Key Features:
- RESTful API endpoints for itinerary generation
- PDF generation for itinerary download
- Popular destinations endpoint
- Comprehensive error handling and validation
- CORS support for frontend integration
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import logging
from datetime import datetime

# Import existing workflow
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graph.workflow import run_workflow
from utils.pdf_generator import generate_pdf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Travel Planner API",
    description="REST API for AI-powered travel itinerary generation using LangGraph and RAG",
    version="1.0.0"
)

# CORS middleware - Configure appropriately for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation
class TravelRequest(BaseModel):
    """
    Request model for travel itinerary generation
    
    Validates incoming travel planning requests with proper constraints
    """
    mode: str = Field(default="seasonal", description="Trip mode (seasonal, short_trip, surprise)")
    starting_place: str = Field(default="Your location", description="Travel origin")
    destination: str = Field(default="", description="Travel destination")
    budget: str = Field(..., description="Travel budget (e.g. '1000 USD' or '50000')")
    days: int = Field(..., gt=0, le=30, description="Number of days for trip")
    people_count: int = Field(default=1, gt=0, description="Number of travellers")
    interests: List[str] = Field(default=[], description="User interest categories")
    dietary_preference: str = Field(default="Both", description="Food preference (Veg, Non-Veg, Both)")
    accommodation_type: str = Field(default="Mid-range", description="Accommodation preference")
    notes: str = Field(default="", description="Additional notes or special requirements")
    include_meals: bool = Field(default=True, description="Include meal plans")
    include_hotel: bool = Field(default=True, description="Include hotel recommendations")
    
    @field_validator('destination')
    @classmethod
    def destination_must_not_be_empty(cls, v: str, info) -> str:
        """Validate that destination is not empty unless in surprise mode"""
        mode = info.data.get('mode', 'seasonal')
        if not v.strip() and mode != 'surprise':
            raise ValueError('Destination cannot be empty')
        return v.strip()

    def get_budget_value(self) -> int:
        """Extract numeric budget value from string"""
        import re
        # Remove commas and other noise
        s = self.budget.replace(',', '')
        # Match the first number
        match = re.search(r'(\d+)', s)
        if match:
            val = int(match.group(1))
            # Handle 'k' or 'lakh'
            if 'k' in s.lower(): val *= 1000
            if 'lakh' in s.lower(): val *= 100000
            return val
        return 50000

    def get_currency_symbol(self) -> str:
        """Extract currency symbol or name from string"""
        s = self.budget.lower()
        if '$' in s or 'dollar' in s: return '$'
        if '€' in s or 'euro' in s: return '€'
        if '£' in s or 'pound' in s: return '£'
        return '₹'


class TravelResponse(BaseModel):
    """
    Response model for travel itinerary
    
    Contains the generated itinerary with all relevant details
    """
    starting_place: str
    destination: str
    duration: str
    itinerary: List[dict]
    total_cost: int
    people_count: int = 1
    currency_symbol: str = "₹"
    budget_breakdown: Optional[dict] = None
    tips: Optional[List[str]] = None
    mode: Optional[str] = "seasonal"
    warning: Optional[str] = None
    generated_at: str


class ChatRequest(BaseModel):
    message: str
    itinerary: dict
    history: List[dict] = []


class HealthResponse(BaseModel):
    """
    Health check response model
    
    Returns API status and version information for monitoring
    """
    status: str
    timestamp: str
    version: str


# API Endpoints
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns API status and version information for monitoring and load balancers.
    This endpoint should be called by monitoring systems to verify API availability.
    
    Returns:
        HealthResponse: Status, timestamp, and version information
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/api/generate-itinerary", response_model=TravelResponse, tags=["Travel"])
async def generate_itinerary(request: TravelRequest):
    """
    Generate travel itinerary based on user preferences
    
    This endpoint coordinates with the LangGraph workflow to generate a
    comprehensive travel itinerary using RAG for context-aware planning.
    
    Args:
        request: TravelRequest with destination, budget, and days
        
    Returns:
        TravelResponse with generated itinerary including day-by-day plans,
        activities, stay information, and meals
        
    Raises:
        HTTPException: If itinerary generation fails or returns invalid structure
    """
    try:
        logger.info(f"Generating itinerary for {request.destination} (Mode: {request.mode}, Days: {request.days})")
        budget_val = request.get_budget_value()
        currency_sym = request.get_currency_symbol()
        
        # Run the LangGraph workflow
        final_plan = run_workflow(
            request.destination,
            budget_val,
            request.days,
            currency_sym,
            starting_place=request.starting_place,
            mode=request.mode,
            people_count=request.people_count,
            interests=request.interests,
            dietary_preference=request.dietary_preference,
            accommodation_type=request.accommodation_type,
            notes=request.notes,
        )
        final_plan["currency_symbol"] = currency_sym
        
        # Validate response structure
        if not final_plan or "itinerary" not in final_plan:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate valid itinerary structure"
            )
        
        # Return formatted response
        return TravelResponse(
            starting_place=final_plan.get("starting_place", request.starting_place),
            destination=final_plan.get("destination", request.destination),
            duration=final_plan.get("duration", f"{request.days}N/{request.days}D"),
            itinerary=final_plan.get("itinerary", []),
            total_cost=final_plan.get("total_cost", budget_val),
            people_count=final_plan.get("people_count", request.people_count),
            currency_symbol=final_plan.get("currency_symbol", currency_sym),
            budget_breakdown=final_plan.get("budget_breakdown"),
            tips=final_plan.get("tips"),
            mode=final_plan.get("mode", request.mode),
            warning=final_plan.get("warning"),
            generated_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error generating itinerary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate itinerary: {str(e)}"
        )


@app.post("/api/generate-pdf", tags=["Travel"])
async def generate_pdf_endpoint(request: TravelRequest):
    """
    Generate PDF for travel itinerary
    
    This endpoint generates a professionally formatted PDF of the travel
    itinerary using ReportLab, suitable for download and printing.
    
    Args:
        request: TravelRequest with destination, budget, and days
        
    Returns:
        PDF file for download with proper content-type headers
        
    Raises:
        HTTPException: If PDF generation fails
    """
    try:
        budget_val = request.get_budget_value()
        currency_sym = request.get_currency_symbol()
        
        # Generate itinerary first
        final_plan = run_workflow(
            request.destination,
            budget_val,
            request.days,
            currency_sym,
            starting_place=request.starting_place,
            mode=request.mode,
            people_count=request.people_count,
            interests=request.interests,
            dietary_preference=request.dietary_preference,
            accommodation_type=request.accommodation_type,
            notes=request.notes,
        )
        final_plan["currency_symbol"] = currency_sym
        
        # Generate PDF using ReportLab
        pdf_filename = f"{request.destination.replace(' ', '_')}_itinerary.pdf"
        pdf_path = generate_pdf(final_plan, pdf_filename)
        
        # Read PDF file for response
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()
        
        # Clean up temporary PDF file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        
        from fastapi.responses import Response
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={pdf_filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )


@app.post("/api/chat", tags=["Travel"])
async def chat_with_itinerary(request: ChatRequest):
    """Chat with the AI about the generated itinerary"""
    try:
        from config import MODEL_NAME
        import ollama
        import json
        
        system_prompt = f"""
        You are 'TRAVEL ITINERARY PLANNER . AI', a premium travel concierge. 
        You have just generated this itinerary for {request.itinerary['destination']} ({request.itinerary['duration']}).
        
        Current Itinerary Context: {json.dumps(request.itinerary)}
        
        Instructions:
        1. Be helpful, enthusiastic, and highly professional.
        2. Answer questions about the locations, activities, or costs in the itinerary.
        3. If the user asks for changes, give them suggestions on how to refine the trip.
        4. Keep your responses vibrant but concise.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in request.history[-5:]: # Keep last 5 messages for context
            messages.append(msg)
        messages.append({"role": "user", "content": request.message})
        
        response = ollama.chat(model=MODEL_NAME, messages=messages)
        return {"response": response["message"]["content"]}
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return {"response": "I'm sorry, I encountered an error while processing your request. How else can I help?"}


@app.get("/api/destinations", tags=["Travel"])
async def get_popular_destinations():
    """
    Get list of popular destinations from the dataset
    
    This endpoint retrieves popular travel destinations from the
    travel packages dataset to help users with suggestions.
    
    Returns:
        JSON object containing list of popular destinations
        
    Note:
        Falls back to hardcoded list if dataset is unavailable
    """
    try:
        import pandas as pd
        df = pd.read_csv("data/travel_packages.csv")
        destinations = df['place'].unique().tolist()[:20]  # Top 20 destinations
        return {"destinations": destinations}
    except Exception as e:
        logger.error(f"Error fetching destinations: {str(e)}")
        # Fallback to hardcoded list
        return {"destinations": ["Manali", "New Delhi", "Jaipur", "Goa", "Kerala", "Coorg"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
