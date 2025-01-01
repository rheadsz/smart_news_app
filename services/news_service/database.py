from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional
from .main import NewsCategory

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/newsdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class NewsArticleDB(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    url = Column(String, unique=True, index=True)
    source = Column(String)
    published_at = Column(DateTime)
    category = Column(SQLAlchemyEnum(NewsCategory), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)
