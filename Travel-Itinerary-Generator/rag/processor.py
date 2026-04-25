def process_text(text, destination):
    if not text:
        return f"Destination: {destination}\n\nNo detailed information found."
        
    return f"""
Destination: {destination}

Key Information:
{text}

Possible Activities:
- sightseeing
- cultural visits
- local exploration
"""
