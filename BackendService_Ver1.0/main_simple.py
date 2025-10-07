from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="Simple Calendar API",
    description="A simple calendar API for managing day-off records",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Simple Calendar API is running", "status": "OK"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Calendar API...")
    print(f"📍 Server will run on: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print("🔄 Database connection will be tested when first endpoint is called")
    
    uvicorn.run(
        "main_simple:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )