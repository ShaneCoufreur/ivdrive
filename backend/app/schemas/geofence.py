import uuid
from datetime import datetime

from pydantic import BaseModel


class GeofenceCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    radius_meters: float
    address: str | None = None


class GeofenceUpdate(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    radius_meters: float | None = None
    address: str | None = None


class GeofenceResponse(BaseModel):
    id: uuid.UUID
    name: str
    latitude: float
    longitude: float
    radius_meters: float
    address: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
