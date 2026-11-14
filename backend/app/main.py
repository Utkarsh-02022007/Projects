# Add your FastAPI application code here.
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, EmergencyContact, Journey #Journey added
from app.schemas import (
    EmergencyContactCreate,
    EmergencyContactUpdate,
    EmergencyContactResponse,
    JourneyCreate,
    JourneyResponse,
)
from sqlalchemy import inspect
from app.database import engine
import app.models

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
# Test whether SQLAlchemy can detect our existing MySQL tables
# Test whether SQLAlchemy can detect our existing MySQL tables
@app.get("/api/test-models")
def test_models():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return {
        "status": "success",
        "database": "MySQL",
        "tables_found": tables,
        "total_tables": len(tables),
        "models_loaded": [
            "User",
            "EmergencyContact",
            "Journey",
            "LocationHistory",
            "AnomalyEvent",
            "RiskAssessment",
            "Notification"
        ]
    }
# ==========================================
# EMERGENCY CONTACT APIs
# ==========================================

# 1. ADD EMERGENCY CONTACT
@app.post(
    "/api/users/{user_id}/emergency-contacts",
    response_model=EmergencyContactResponse
)
def add_emergency_contact(
    user_id: int,
    contact_data: EmergencyContactCreate,
    db: Session = Depends(get_db)
):
    # Check whether the user exists
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Only one contact should be primary per user
    if contact_data.is_primary:
        db.query(EmergencyContact).filter(
            EmergencyContact.user_id == user_id
        ).update({"is_primary": False})

    new_contact = EmergencyContact(
        user_id=user_id,
        contact_name=contact_data.contact_name,
        phone=contact_data.phone,
        relationship=contact_data.relationship,
        is_primary=contact_data.is_primary
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


# 2. GET ALL EMERGENCY CONTACTS
@app.get(
    "/api/users/{user_id}/emergency-contacts",
    response_model=list[EmergencyContactResponse]
)
def get_emergency_contacts(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == user_id
    ).all()

    return contacts


# 3. UPDATE EMERGENCY CONTACT
@app.put(
    "/api/users/{user_id}/emergency-contacts/{contact_id}",
    response_model=EmergencyContactResponse
)
def update_emergency_contact(
    user_id: int,
    contact_id: int,
    contact_data: EmergencyContactUpdate,
    db: Session = Depends(get_db)
):
    contact = db.query(EmergencyContact).filter(
        EmergencyContact.id == contact_id,
        EmergencyContact.user_id == user_id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Emergency contact not found"
        )

    update_data = contact_data.model_dump(exclude_unset=True)

    if update_data.get("is_primary") is True:
        db.query(EmergencyContact).filter(
            EmergencyContact.user_id == user_id,
            EmergencyContact.id != contact_id
        ).update({"is_primary": False})

    for key, value in update_data.items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)

    return contact


# 4. DELETE EMERGENCY CONTACT
@app.delete("/api/users/{user_id}/emergency-contacts/{contact_id}")
def delete_emergency_contact(
    user_id: int,
    contact_id: int,
    db: Session = Depends(get_db)
):
    contact = db.query(EmergencyContact).filter(
        EmergencyContact.id == contact_id,
        EmergencyContact.user_id == user_id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Emergency contact not found"
        )

    db.delete(contact)
    db.commit()

    return {
        "message": "Emergency contact deleted successfully"
    }

# ==========================================
# JOURNEY MANAGEMENT APIs
# ==========================================

from datetime import datetime


# 1. START A NEW JOURNEY
@app.post(
    "/api/users/{user_id}/journeys",
    response_model=JourneyResponse
)
def start_journey(
    user_id: int,
    journey_data: JourneyCreate,
    db: Session = Depends(get_db)
):
    # Check whether user exists
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Prevent multiple active journeys
    active_journey = db.query(Journey).filter(
        Journey.user_id == user_id,
        Journey.status == "active"
    ).first()

    if active_journey:
        raise HTTPException(
            status_code=400,
            detail="You already have an active journey"
        )

    # Validate expected arrival
    if journey_data.expected_arrival <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Expected arrival must be in the future"
        )

    new_journey = Journey(
        user_id=user_id,
        start_location=journey_data.start_location,
        destination=journey_data.destination,
        expected_arrival=journey_data.expected_arrival,
        status="active"
    )

    db.add(new_journey)
    db.commit()
    db.refresh(new_journey)

    return new_journey


# 2. GET ALL JOURNEYS
@app.get(
    "/api/users/{user_id}/journeys",
    response_model=list[JourneyResponse]
)
def get_journeys(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    journeys = db.query(Journey).filter(
        Journey.user_id == user_id
    ).order_by(Journey.start_time.desc()).all()

    return journeys


# 3. GET ACTIVE JOURNEY
@app.get(
    "/api/users/{user_id}/journeys/active",
    response_model=JourneyResponse
)
def get_active_journey(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    journey = db.query(Journey).filter(
        Journey.user_id == user_id,
        Journey.status == "active"
    ).first()

    if not journey:
        raise HTTPException(
            status_code=404,
            detail="No active journey found"
        )

    return journey


# 4. END A JOURNEY
@app.put(
    "/api/users/{user_id}/journeys/{journey_id}/end",
    response_model=JourneyResponse
)
def end_journey(
    user_id: int,
    journey_id: int,
    db: Session = Depends(get_db)
):
    journey = db.query(Journey).filter(
        Journey.id == journey_id,
        Journey.user_id == user_id
    ).first()

    if not journey:
        raise HTTPException(
            status_code=404,
            detail="Journey not found"
        )

    if journey.status != "active":
        raise HTTPException(
            status_code=400,
            detail="Journey is not active"
        )

    journey.actual_arrival = datetime.now()
    journey.status = "completed"

    db.commit()
    db.refresh(journey)

    return journey

