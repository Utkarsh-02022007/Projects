from pydantic import BaseModel, ConfigDict, Field


class EmergencyContactCreate(BaseModel):
    contact_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=1, max_length=20)
    relationship: str | None = Field(default=None, max_length=100)
    is_primary: bool = False


class EmergencyContactUpdate(BaseModel):
    contact_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, min_length=1, max_length=20)
    relationship: str | None = Field(default=None, max_length=100)
    is_primary: bool | None = None


class EmergencyContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    contact_name: str
    phone: str
    relationship: str | None
    is_primary: bool
from datetime import datetime


class JourneyCreate(BaseModel):
    start_location: str = Field(min_length=1, max_length=200)
    destination: str = Field(min_length=1, max_length=200)
    expected_arrival: datetime


class JourneyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    start_location: str
    destination: str | None
    start_time: datetime
    expected_arrival: datetime
    actual_arrival: datetime | None
    status: str