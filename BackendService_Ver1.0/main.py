from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        from app.db.database import engine
        from app.models.dayoff import Base
        
        # Test database connection
        with engine.connect() as connection:
            logger.info("✅ Database connection successful!")
            
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created/verified!")
        
        # Include API routes
        from app.api.dayoff import router as dayoff_router
        app.include_router(dayoff_router)
        logger.info("✅ API routes loaded!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        logger.info("🔄 API will run without database endpoints for now")

@app.get("/")
async def root():
    return {
        "message": "Simple Calendar API is running", 
        "status": "OK",
        "version": "1.0.0",
        "docs": f"http://{settings.HOST}:{settings.PORT}/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from app.db.database import engine
        with engine.connect() as connection:
            db_status = "connected"
    except:
        db_status = "disconnected"
        
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": db_status
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Calendar API...")
    print(f"📍 Server will run on: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )