from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime
import requests

class NewsCategory(str, Enum):
    #creating fixed set of categories for news articles
    BUSINESS = "business"
    TECHNOLOGY = "technology"
    SCIENCE = "science"
    HEALTH = "health"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"


class NewsArticle(BaseModel):
    title: str = Field(..., description="The headline or title of the news article")
    description: Optional[str] = Field(None, description="A brief description of the news article")
    url: str = Field(..., description="The URL to the full article")
    source: str = Field(..., description="The source/publisher of the article")
    published_at: datetime = Field(..., description="Publication date and time")
    category: Optional[NewsCategory] = Field(None, description="The category of the news article")

    class Config:
        schema_extra = {
            "example": {
                "title": "SpaceX Successfully Launches Satellite",
                "description": "SpaceX's Falcon 9 rocket successfully launched a communications satellite into orbit",
                "url": "https://example.com/spacex-launch",
                "source": "Space News",
                "published_at": "2025-01-01T12:00:00Z",
                "category": "technology"
            }
        }

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")

app = FastAPI(
    title="Smart News API",
    description="API for aggregating and serving news articles from various sources",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(
    "/api/news",
    response_model=List[NewsArticle],
    responses={
        200: {
            "description": "List of news articles",
            "content": {
                "application/json": {
                    "example": [{
                        "title": "SpaceX Successfully Launches Satellite",
                        "description": "SpaceX's Falcon 9 rocket successfully launched a communications satellite into orbit",
                        "url": "https://example.com/spacex-launch",
                        "source": "Space News",
                        "published_at": "2025-01-01T12:00:00Z",
                        "category": "technology"
                    }]
                }
            }
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    },
    summary="Get news articles",
    description="Retrieve a list of news articles, optionally filtered by category"
)
async def get_news(
    category: Optional[NewsCategory] = Query(
        None,
        description="Filter articles by category"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of articles to return"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of articles to skip"
    )
):
    try:
        # Placeholder for actual news API integration
        articles = [
            {
                "title": "Sample News Article",
                "description": "This is a sample news article description",
                "url": "https://example.com",
                "source": "Sample Source",
                "published_at": datetime.now(),
                "category": category or NewsCategory.TECHNOLOGY
            }
        ]
        return articles[offset:offset + limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    "/api/news/categories",
    response_model=List[NewsCategory],
    summary="Get available news categories",
    description="Retrieve a list of all available news categories"
)
async def get_categories():
    return list(NewsCategory)

@app.get(
    "/api/news/{article_id}",
    response_model=NewsArticle,
    responses={
        404: {
            "description": "Article not found",
            "model": ErrorResponse
        }
    },
    summary="Get news article by ID",
    description="Retrieve a specific news article by its ID"
)
async def get_article(
    article_id: str = Path(..., description="The ID of the article to retrieve")
):
    # Placeholder for database lookup
    article = {
        "title": f"Article {article_id}",
        "description": "This is a sample article",
        "url": f"https://example.com/article/{article_id}",
        "source": "Sample Source",
        "published_at": datetime.now(),
        "category": NewsCategory.TECHNOLOGY
    }
    return article

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
