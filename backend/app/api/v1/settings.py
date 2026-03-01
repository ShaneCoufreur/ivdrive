import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_active_user
from app.database import get_db
from app.models.geofence import Geofence
from app.models.user import User
from app.schemas.geofence import GeofenceCreate, GeofenceResponse, GeofenceUpdate

router = APIRouter()


@router.get("/geofences", response_model=list[GeofenceResponse])
async def list_geofences(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Geofence).where(Geofence.user_id == user.id)
    )
    return result.scalars().all()


@router.post(
    "/geofences",
    response_model=GeofenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_geofence(
    body: GeofenceCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    geofence = Geofence(
        user_id=user.id,
        name=body.name,
        latitude=body.latitude,
        longitude=body.longitude,
        radius_meters=body.radius_meters,
        address=body.address,
    )
    db.add(geofence)
    await db.flush()
    return geofence


@router.put("/geofences/{geofence_id}", response_model=GeofenceResponse)
async def update_geofence(
    geofence_id: uuid.UUID,
    body: GeofenceUpdate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Geofence).where(
            Geofence.id == geofence_id, Geofence.user_id == user.id
        )
    )
    geofence = result.scalar_one_or_none()
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(geofence, field, value)
    await db.flush()
    return geofence


@router.delete(
    "/geofences/{geofence_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_geofence(
    geofence_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Geofence).where(
            Geofence.id == geofence_id, Geofence.user_id == user.id
        )
    )
    geofence = result.scalar_one_or_none()
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    await db.delete(geofence)
    await db.flush()
