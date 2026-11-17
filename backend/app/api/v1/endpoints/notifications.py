"""
AgriMate AI - Notification Endpoints (Phase 6)
In-App notification inbox and simulated FCM push dispatch integration.
"""

from typing import List, Optional, Any, Dict
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.notification import Notification
from app.api.v1.endpoints.auth import get_current_user
from app.services.notification_service import NotificationService
from app.schemas.common import APIResponse

router = APIRouter(prefix="/notifications", tags=["Notifications & FCM Push"])


class TestFcmRequest(BaseModel):
    title: str = Field(..., example="Crop Price Surge Alert")
    message: str = Field(..., example="Potato prices rose 4.5% in Okara Mandi today.")
    notification_type: str = Field("SYSTEM", example="PRICE_ALERT")


@router.get("", response_model=APIResponse[List[Dict[str, Any]]])
def get_user_notifications(
    unread_only: bool = False,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetches the persistent in-app notifications for the logged-in user.
    """
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    if unread_only:
        query = query.filter(Notification.is_read == False)

    notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()

    results = []
    for n in notifications:
        extra_data = {}
        if n.data_json:
            try:
                extra_data = json.loads(n.data_json)
            except Exception:
                extra_data = {}

        results.append({
            "id": n.id,
            "title": n.title,
            "title_ur": n.title_ur,
            "message": n.message,
            "message_ur": n.message_ur,
            "notification_type": n.notification_type,
            "data": extra_data,
            "is_read": n.is_read,
            "fcm_message_id": n.fcm_message_id,
            "fcm_dispatched": n.fcm_dispatched,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M")
        })

    return APIResponse(data=results, message="Notifications retrieved successfully")


@router.put("/{notification_id}/read", response_model=APIResponse[Dict[str, Any]])
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Marks a notification as read.
    """
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    notif.is_read = True
    db.commit()

    return APIResponse(
        data={"id": notif.id, "is_read": True},
        message="Notification marked as read"
    )


@router.post("/mark-all-read", response_model=APIResponse[Dict[str, Any]])
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Marks all notifications for the current user as read.
    """
    updated_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True})

    db.commit()

    return APIResponse(
        data={"updated_count": updated_count},
        message="All notifications marked as read"
    )


@router.post("/test-fcm", response_model=APIResponse[Dict[str, Any]])
def test_fcm_dispatch(
    payload: TestFcmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Simulates sending an FCM push notification and stores it in the in-app inbox.
    """
    notif = NotificationService.create_notification(
        db=db,
        user_id=current_user.id,
        title=payload.title,
        message=payload.message,
        notification_type=payload.notification_type,
        data={"source": "fcm_test"}
    )

    return APIResponse(
        data={
            "id": notif.id,
            "title": notif.title,
            "fcm_message_id": notif.fcm_message_id,
            "fcm_dispatched": notif.fcm_dispatched,
            "created_at": notif.created_at.isoformat()
        },
        message="FCM push notification simulated successfully"
    )
