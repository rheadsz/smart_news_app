from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import logging
import re
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
            "pageSize": 20,
            "country": "us"
        }
        
        if category and category.lower() != "all":
            params["category"] = category

        # Make the request to NewsAPI
        response = requests.get(base_url, params=params)
        logger.info(f"NewsAPI Response Status: {response.status_code}")
        
        if response.status_code == 200:
            news_data = response.json()
            articles = []
            
            # Log a sample article for debugging
            if news_data.get("articles"):
                sample = news_data["articles"][0]
                logger.info(f"""
                Sample Article:
                Title: {sample.get('title')}
                URL: {sample.get('url')}
                Image URL: {sample.get('urlToImage')}
                Source: {sample.get('source', {}).get('name')}
                """)
            
            for idx, article in enumerate(news_data.get("articles", [])):
                if article.get("title") and article.get("title") != "[Removed]":
                    # Get the image URL directly from the article
                    image_url = article.get("urlToImage")
                    
                    # Log the image URL we're using
                    logger.info(f"""
                    Article {idx + 1}:
                    Title: {article.get('title')}
                    Original Image URL: {image_url}
                    """)
                    
                    # Only use the image if it's a valid URL
                    if not image_url or "http" not in str(image_url):
                        # Use a category-specific image
                        category_images = {
                            "business": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab",
                            "entertainment": "https://images.unsplash.com/photo-1603190287605-e6ade32fa852",
                            "health": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528",
                            "science": "https://images.unsplash.com/photo-1507413245164-6160d8298b31",
                            "sports": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211",
                            "technology": "https://images.unsplash.com/photo-1518770660439-4636190af475"
                        }
                        
                        # Get default image for category or general news image
                        image_url = category_images.get(
                            category,
                            "https://images.unsplash.com/photo-1495020689067-958852a7765e"  # Default news image
                        )
                        logger.info(f"Using category fallback image for {article.get('title')}: {image_url}")
                    
                    article_obj = NewsArticle(
                        title=article.get("title", ""),
                        description=article.get("description", "No description available"),
                        url=article.get("url", ""),
                        source=article.get("source", {}).get("name", "Unknown Source"),
                        published_at=article.get("publishedAt", ""),
                        category=category,
                        image_url=image_url
                    )
                    articles.append(article_obj)
            
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
