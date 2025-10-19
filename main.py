# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import blog_tools

# Create FastAPI application instance
app = FastAPI(
    title="Blog Title Generator API",
    description="Generate SEO-optimized blog titles using OpenAI",
    version="1.0.0"
)

# Configure CORS (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include our blog tools routes
app.include_router(
    blog_tools.router,
    prefix="/api",  # All routes start with /api
    tags=["blog_tools"]  # Group in API docs
)

# Root endpoint (for testing if API is running)
@app.get("/")
async def root():
    return {
        "message": "Blog Title Generator API is running!",
        "endpoints": {
            "generate_titles": "/api/blog/generate-titles?user_topic=YOUR_TOPIC"
        }
    }


# Run the application (only when running directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)