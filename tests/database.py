# tests/test_database.py

import pytest
from services.news_service.database import SessionLocal, NewsArticleDB
from services.news_service.main import NewsCategory

@pytest.fixture(scope="module")
def db_session():
    # Create a new session for the tests
    session = SessionLocal()
    yield session
    session.close()

def test_create_article(db_session):
    article = NewsArticleDB(title="Test Article", description="A test article", url="http://example.com", source="Test Source")
    db_session.add(article)
    db_session.commit()
    assert article.id is not None  # Ensure the article has been created with an ID

def test_get_article(db_session):
    article = db_session.query(NewsArticleDB).filter(NewsArticleDB.title == "Test Article").first()
    assert article is not None
    assert article.title == "Test Article"