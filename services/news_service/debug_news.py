from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specifically allow our frontend
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

NEWS_API_KEY = "38d6208ab04e4ab9b05846ec5fbceb8f"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

@app.get("/")
async def root():
    return {"message": "News API is running"}

@app.get("/api/news", response_model=List[NewsArticle])
async def get_news(category: Optional[str] = None):
    try:
        logger.info(f"Fetching news for category: {category}")
        
        params = {
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": 10,
            "country": "us"  # Added country parameter
        }
        
        if category:
            params["category"] = category

        logger.info(f"Making request to NewsAPI with params: {params}")
        
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        
        news_data = response.json()
        logger.info(f"Received {len(news_data.get('articles', []))} articles from NewsAPI")
        
        articles = []
        for article in news_data.get("articles", []):
            articles.append(NewsArticle(
                title=article.get("title", ""),
                description=article.get("description"),
                url=article.get("url", ""),
                source=article.get("source", {}).get("name", "Unknown"),
                published_at=article.get("publishedAt", ""),
                category=category
            ))
        
        return articles
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to NewsAPI: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting news service...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
