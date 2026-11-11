# Add your FastAPI application code here.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import test_database_connection

app = FastAPI(
    title="SafeHer AI",
    description="Personal Safety and Risk Detection System",
    version="1.0.0",
)

# Allow the React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home route
@app.get("/")
def home():
    return {
        "message": "SafeHer AI Backend is running!"
    }


# API health check
@app.get("/api/health")
def health_check():
    return {
        "status": "running",
        "application": "SafeHer AI",
    }


# MySQL connection test
@app.get("/api/test-db")
def test_db():
    try:
        result = test_database_connection()

        return {
            "status": "success",
            "database": "MySQL",
            "connection": "Connected successfully",
            "test_result": result,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed. Check MySQL and backend configuration.",
        )
