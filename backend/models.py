from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Incident(BaseModel):
    device_name: str
    location: str
    incident_type: str
    severity: str       # low, medium, high, critical
    description: str
    status: str = "open"