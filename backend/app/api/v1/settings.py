import uuid
import os
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_active_user
from app.database import get_db
from app.models.geofence import Geofence
from app.models.user import User
from app.schemas.geofence import GeofenceCreate, GeofenceResponse, GeofenceUpdate
from app.services.export import ExportService

router = APIRouter()

# ── Data Export ─────────────────────────────────────────────────────────────

@router.post("/export", status_code=status.HTTP_202_ACCEPTED)
async def request_data_export(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Triggers a 1-year data export for the user.
    In a real-world scenario, this would be a background task.
    For this implementation, we will generate it synchronously to provide 
    an immediate download link in the first version.
    """
    service = ExportService(db)
    zip_path = await service.generate_user_export(user.id)
    
    if not zip_path:
        raise HTTPException(status_code=404, detail="No vehicle data found to export")
    
    # We return the file directly for now. 
    # In Phase 2, this will be handled via status polling.
    return FileResponse(
        path=zip_path,
        filename=os.path.basename(zip_path),
        media_type="application/zip"
    )

# ── Geofences ───────────────────────────────────────────────────────────────

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
