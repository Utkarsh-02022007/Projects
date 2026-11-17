

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Text,
    DateTime,
    Boolean,
    DECIMAL,
    ForeignKey,
    text
)
from sqlalchemy.orm import relationship as db_relationship

from app.database import Base


# -------------------------
# 1. USERS
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    emergency_contacts = db_relationship(
        "EmergencyContact",
        back_populates="user"
    )

    journeys = db_relationship(
        "Journey",
        back_populates="user"
    )

    notifications = db_relationship(
        "Notification",
        back_populates="user"
    )


# -------------------------
# 2. EMERGENCY CONTACTS
# -------------------------

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    contact_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    relationship = Column(String(100), nullable=True)
    is_primary = Column(Boolean, server_default=text("0"))
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    user = db_relationship(
        "User",
        back_populates="emergency_contacts"
    )


# -------------------------
# 3. JOURNEYS
# -------------------------

class Journey(Base):
    __tablename__ = "JOURNEY"

    id = Column(Integer, primary_key=True, autoincrement=True)
    destination = Column(String(200), nullable=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    start_location = Column(String(200), nullable=False)
    start_time = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    expected_arrival = Column(DateTime, nullable=False)
    actual_arrival = Column(DateTime, nullable=True)
    status = Column(String(20), server_default=text("'active'"))

    user = db_relationship(
        "User",
        back_populates="journeys"
    )

    locations = db_relationship(
        "LocationHistory",
        back_populates="journey"
    )

    anomaly_events = db_relationship(
        "AnomalyEvent",
        back_populates="journey"
    )

    risk_assessments = db_relationship(
        "RiskAssessment",
        back_populates="journey"
    )

    notifications = db_relationship(
        "Notification",
        back_populates="journey"
    )


# -------------------------
# 4. LOCATION HISTORY
# -------------------------

class LocationHistory(Base):
    __tablename__ = "location_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    journey_id = Column(
        Integer,
        ForeignKey("JOURNEY.id", ondelete="CASCADE"),
        nullable=False
    )
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    recorded_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    journey = db_relationship(
        "Journey",
        back_populates="locations"
    )


# -------------------------
# 5. ANOMALY EVENTS
# -------------------------

class AnomalyEvent(Base):
    __tablename__ = "anomaly_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    journey_id = Column(
        Integer,
        ForeignKey("JOURNEY.id", ondelete="CASCADE"),
        nullable=False
    )
    event_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(20), server_default=text("'low'"))
    detected_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    status = Column(String(30), server_default=text("'pending'"))

    journey = db_relationship(
        "Journey",
        back_populates="anomaly_events"
    )

    risk_assessments = db_relationship(
        "RiskAssessment",
        back_populates="anomaly_event"
    )


# -------------------------
# 6. RISK ASSESSMENT
# -------------------------

class RiskAssessment(Base):
    __tablename__ = "risk_assessment"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    journey_id = Column(
        Integer,
        ForeignKey("JOURNEY.id", ondelete="CASCADE"),
        nullable=False
    )
    anomaly_id = Column(
        BigInteger,
        ForeignKey("anomaly_events.id", ondelete="SET NULL"),
        nullable=True
    )
    risk_score = Column(DECIMAL(5, 2), nullable=False)
    risk_level = Column(String(20), nullable=False)
    explanation = Column(Text, nullable=True)
    assessed_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    journey = db_relationship(
        "Journey",
        back_populates="risk_assessments"
    )

    anomaly_event = db_relationship(
        "AnomalyEvent",
        back_populates="risk_assessments"
    )

    notifications = db_relationship(
        "Notification",
        back_populates="risk_assessment"
    )


# -------------------------
# 7. NOTIFICATIONS
# -------------------------

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    journey_id = Column(
        Integer,
        ForeignKey("JOURNEY.id", ondelete="SET NULL"),
        nullable=True
    )
    risk_assessment_id = Column(
        BigInteger,
        ForeignKey("risk_assessment.id", ondelete="SET NULL"),
        nullable=True
    )
    recipient_phone = Column(String(20), nullable=False)
    message_text = Column(Text, nullable=False)
    notification_type = Column(String(30), nullable=False)
    delivery_status = Column(
        String(30),
        server_default=text("'pending'")
    )
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    user = db_relationship(
        "User",
        back_populates="notifications"
    )

    journey = db_relationship(
        "Journey",
        back_populates="notifications"
    )

    risk_assessment = db_relationship(
        "RiskAssessment",
        back_populates="notifications"
    )

#hello

