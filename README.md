# Smart News App

A modern news aggregation platform built with microservices architecture.

## Architecture Overview

- Frontend: React.js with TypeScript
- Backend Services:
  - News Service (FastAPI)
  - User Service (FastAPI)
  - Recommendation Service (FastAPI)
- Message Broker: Apache Kafka
- Caching: Redis
- Databases:
  - PostgreSQL (User data & news metadata)
  - MongoDB (News content)
- Deployment: Docker & Kubernetes

## Features

- Real-time news aggregation from multiple sources
- Personalized news feed
- Category-based filtering
- Search functionality
- User preferences and bookmarks
- News recommendation system

## Setup Instructions

1. Clone the repository
2. Install dependencies for each service
3. Set up Docker containers
4. Run the development environment

Detailed setup instructions for each component are available in their respective directories.

## Project Structure

```
smart_news_app/
├── frontend/                 # React frontend application
├── services/
│   ├── news_service/        # News aggregation and management
│   ├── user_service/        # User management and authentication
│   └── recommendation/      # News recommendation engine
├── infrastructure/
│   ├── kafka/              # Kafka configuration
│   └── kubernetes/         # K8s deployment configs
└── docker/                 # Docker configurations
```

## API Documentation

API documentation is available at `/api/docs` when running each service.

## Development

Check individual service READMEs for specific development instructions.
