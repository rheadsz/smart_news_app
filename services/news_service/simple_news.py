from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://smart-news-app.netlify.app",  # Production frontend
        "http://localhost:3000",  # Local development
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    source: str
    published_at: str
    category: Optional[str] = None
    image_url: Optional[str] = None

# Get API key from environment variable
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY environment variable is not set")

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

@app.get("/api/news", response_model=List[NewsArticle])
async def get_news(category: Optional[str] = None):
    try:
        # Build the API URL
        base_url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": 20
        }
        
        if category and category.lower() != "all":
            params["category"] = category

        # Make the request to NewsAPI
        response = requests.get(base_url, params=params)
        
        # Log the response for debugging
        logger.info(f"NewsAPI Response Status: {response.status_code}")
        
        if response.status_code == 200:
            news_data = response.json()
            
            # Log the first article for debugging
            if news_data.get("articles"):
                first_article = news_data["articles"][0]
                logger.info(f"Sample Article: Title: {first_article.get('title')}, Image: {first_article.get('urlToImage')}")
            
            articles = []
            for article in news_data.get("articles", []):
                if article.get("title") and article.get("title") != "[Removed]":
                    # Get the image URL with a default fallback
                    image_url = article.get("urlToImage")
                    if not image_url or "http" not in str(image_url):
                        image_url = "https://placehold.co/600x400?text=News"
                    
                    articles.append(NewsArticle(
                        title=article.get("title", ""),
                        description=article.get("description", "No description available"),
                        url=article.get("url", ""),
                        source=article.get("source", {}).get("name", "Unknown Source"),
                        published_at=article.get("publishedAt", ""),
                        category=category,
                        image_url=image_url
                    ))
            
            return articles
        else:
            logger.error(f"NewsAPI Error: Status {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Error fetching news from external API")
            
    except Exception as e:
        logger.error(f"Error in get_news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news")
async def get_news(category: Optional[str] = None):
    try:
        # Build the API URL
        base_url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": 20
        }
        
        if category and category.lower() != "all":
            params["category"] = category

        # Make the request to NewsAPI
        response = requests.get(base_url, params=params)
        
        # Log the response for debugging
        logger.info(f"NewsAPI Response Status: {response.status_code}")
        
        if response.status_code == 200:
            news_data = response.json()
            
            # Log the first article for debugging
            if news_data.get("articles"):
                first_article = news_data["articles"][0]
                logger.info(f"Sample Article: Title: {first_article.get('title')}, Image: {first_article.get('urlToImage')}")
            
            articles = []
            for article in news_data.get("articles", []):
                if article.get("title") and article.get("title") != "[Removed]":
                    # Get the image URL with a default fallback
                    image_url = article.get("urlToImage")
                    if not image_url or "http" not in str(image_url):
                        image_url = "https://placehold.co/600x400?text=News"
                    
                    articles.append(NewsArticle(
                        title=article.get("title", ""),
                        description=article.get("description", "No description available"),
                        url=article.get("url", ""),
                        source=article.get("source", {}).get("name", "Unknown Source"),
                        published_at=article.get("publishedAt", ""),
                        category=category,
                        image_url=image_url
                    ))
            
            return articles
        else:
            logger.error(f"NewsAPI Error: Status {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Error fetching news from external API")
            
    except Exception as e:
        logger.error(f"Error in get_news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
