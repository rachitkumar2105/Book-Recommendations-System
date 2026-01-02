from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

# Import recommender logic
# Note: When running from root with `uvicorn backend.main:app`, this import works
from backend.recommender import get_trending, get_book_titles, recommend_by_title

app = FastAPI(title="Book Recommendation API")

# Allow CORS for development convenience (though we serve static files from same origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Book(BaseModel):
    title: str
    author: str
    avg_rating: float
    rating_count: float

class RecommendationRequest(BaseModel):
    title: str

@app.get("/api/trending", response_model=List[Book])
def api_trending():
    """Get top 12 trending books"""
    df = get_trending(12)
    return df.to_dict(orient="records")

@app.get("/api/books", response_model=List[str])
def api_books():
    """Get all book titles for autocomplete"""
    return get_book_titles()

@app.post("/api/recommend", response_model=List[Book])
def api_recommend(request: RecommendationRequest):
    """Get recommendations based on a book title"""
    try:
        recs = recommend_by_title(request.title)
        if recs is None or recs.empty:
            raise HTTPException(status_code=404, detail="Book not found or no recommendations available")
        return recs.to_dict(orient="records")
    except Exception as e:
        print(f"Error recommending for {request.title}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount frontend directory for static file serving
# This must be last to allow API routes to take precedence
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
else:
    print("Warning: 'frontend' directory not found. Static files will not be served.")
