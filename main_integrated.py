from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chat_summary.routes import router as chat_router
from search_agent.routes import router as research_router
from recommendation.routes import router as recommendation_router
from clustering.routes import router as clustering_router

app = FastAPI(
    title="EventHub AI API",
    description="EventHub AI - Integrated API for chat summarization, search agents, recommendations, and dynamic pricing.",
    version="0.1.0"
)

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(chat_router, prefix="/chat", tags=["Chat Summary"])
app.include_router(research_router, prefix="/research", tags=["Search Agent"])
app.include_router(recommendation_router, prefix="/recommendation", tags=["Recommendation"])
app.include_router(clustering_router, prefix="/pricing", tags=["Dynamic Pricing"])

@app.get("/")
def root():
    return {
        "message": "Welcome to the EventHub AI API",
        "version": "0.1.0",
        "features": {
            "chat_summary": "Summarize chat histories",
            "search_agent": "Research and search capabilities",
            "recommendation": "Event recommendations based on user preferences",
            "dynamic_pricing": "Price adjustments based on user metadata clustering"
        },
        "endpoints": {
            "chat": "/chat/...",
            "research": "/research/...",
            "recommendation": "/recommendation/...",
            "pricing": "/pricing/adjust-price"
        },
        "documentation": "/docs"
    }
