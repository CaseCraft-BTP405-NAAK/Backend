import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import database and models
from app.db import engine, Base
from app.models import User, Product

# Import routes
from app.routes import products, auth

# Load environment variables
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Casecraft API",
    description="E-commerce API for Casecraft",
    version="0.1.0"
)

# Configure CORS for development and production
origins = [
    "http://localhost:3000",  # Local development frontend
    "https://casecraft.netlify.app",  # Production frontend (example)
    "*"  # Allow all origins for development (remove in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/", summary="Root endpoint", description="Returns a welcome message and API status")
async def root():
    """Root endpoint that confirms the API is running.
    
    Returns:
        dict: A message indicating the API is operational
    """
    return {
        "message": "Welcome to Casecraft API", 
        "status": "operational",
        "version": "0.1.0"
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 