import secrets
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.invite import InviteRequest
from app.models.user import User
from app.api.v1.dependencies import get_current_superuser
from app.schemas.invite import (
    InviteRequestResponse,
    InviteApprovalRequest,
    PromoteUserRequest
)
from app.config import settings
from app.services.email import send_invite_email

router = APIRouter()

@router.get("/invites", response_model=list[InviteRequestResponse])
async def list_invites(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_superuser)
):
    result = await db.execute(select(InviteRequest).order_by(InviteRequest.created_at.desc()))
    return result.scalars().all()

@router.post("/invites/approve")
async def approve_invite(
    body: InviteApprovalRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_superuser)
):
    result = await db.execute(select(InviteRequest).where(InviteRequest.email == body.email))
    invite = result.scalar_one_or_none()
    
    if not invite:
        raise HTTPException(status_code=404, detail="Invite request not found")
    
    if invite.status != "pending":
        raise HTTPException(status_code=400, detail=f"Invite is already {invite.status}")

    token = secrets.token_urlsafe(32)
    invite.status = "approved"
    invite.token = token
    invite.approved_at = datetime.utcnow()
    
    await db.commit()
    
    invite_link = f"{settings.app_base_url}/register?token={token}"

    email_sent = send_invite_email(body.email, invite_link)

    return {
        "message": "Invite approved",
        "invite_link": invite_link,
        "email_sent": email_sent,
    }

@router.post("/invites/reject")
async def reject_invite(
    body: InviteApprovalRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_superuser),
):
    result = await db.execute(select(InviteRequest).where(InviteRequest.email == body.email))
    invite = result.scalar_one_or_none()

    if not invite:
        raise HTTPException(status_code=404, detail="Invite request not found")

    if invite.status != "pending":
        raise HTTPException(status_code=400, detail=f"Invite is already {invite.status}")

    invite.status = "rejected"
    await db.commit()

    return {"message": f"Invite for {body.email} rejected"}


@router.get("/users")
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_superuser),
):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [
        {
            "id": str(u.id),
            "email": u.email,
            "display_name": u.display_name,
            "is_active": u.is_active,
            "is_superuser": u.is_superuser,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]


@router.post("/users/promote")
async def promote_user(
    body: PromoteUserRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_superuser)
):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_superuser = True
    await db.commit()
    
    return {"message": f"User {body.email} promoted to superuser"}


@router.post("/users/demote")
async def demote_user(
    body: PromoteUserRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_superuser),
):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_superuser = False
    await db.commit()

    return {"message": f"User {body.email} demoted from superuser"}
