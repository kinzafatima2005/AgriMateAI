"""
AgriMate AI - Notification Service
In-App persistent notifications and simulated Google Firebase Cloud Messaging (FCM HTTP v1) push dispatch.
"""

import json
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models.notification import Notification

logger = logging.getLogger("agrimate.notifications")


class NotificationService:

    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "SYSTEM",
        title_ur: Optional[str] = None,
        message_ur: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        device_token: Optional[str] = None
    ) -> Notification:
        """
        Creates an in-app notification record and simulates an FCM HTTP v1 push dispatch.
        """
        # 1. Simulate FCM message dispatch
        fcm_id = f"fcm-msg-{uuid.uuid4().hex[:12]}"
        simulated_token = device_token or f"fcm-token-user-{user_id}"

        fcm_payload = {
            "message": {
                "token": simulated_token,
                "notification": {
                    "title": title,
                    "body": message
                },
                "data": {
                    "notification_type": notification_type,
                    "user_id": str(user_id),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    **(data or {})
                },
                "android": {
                    "priority": "high",
                    "notification": {
                        "channel_id": "agrimate_primary_channel",
                        "sound": "default",
                        "icon": "ic_notification"
                    }
                }
            }
        }

        # Log simulated FCM dispatch
        logger.info(f"[FCM_SIMULATOR] Dispatched push message {fcm_id} to token {simulated_token}: {title}")

        # 2. Persist in-app notification record
        notif = Notification(
            user_id=user_id,
            title=title,
            title_ur=title_ur or title,
            message=message,
            message_ur=message_ur or message,
            notification_type=notification_type,
            data_json=json.dumps(data) if data else None,
            fcm_message_id=fcm_id,
            fcm_dispatched=True,
            is_read=False,
            created_at=datetime.now(timezone.utc)
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)
        return notif

    @staticmethod
    def notify_expert_review(
        db: Session,
        farmer_id: int,
        scan_id: int,
        disease_name: str,
        expert_name: str = "Agronomist Dr. Tariq (Extension Officer)"
    ) -> Notification:
        """
        Notifies a farmer that their flagged leaf scan has been reviewed by an agricultural expert.
        """
        title = "Expert Agronomist Scan Review Completed"
        title_ur = "زرعی ماہر کا اسکین جائزہ مکمل"
        msg = f"Your scan #{scan_id} was reviewed by {expert_name}. Verified diagnosis: {disease_name}. View recommended prescription."
        msg_ur = f"آپ کے اسکین #{scan_id} کا ماہر {expert_name} نے معائنہ مکمل کر لیا ہے۔ تصدیق شدہ تشخیص: {disease_name}۔"

        return NotificationService.create_notification(
            db=db,
            user_id=farmer_id,
            title=title,
            title_ur=title_ur,
            message=msg,
            message_ur=msg_ur,
            notification_type="EXPERT_REVIEW",
            data={"scan_id": str(scan_id), "disease": disease_name}
        )

    @staticmethod
    def notify_buyer_match(
        db: Session,
        farmer_id: int,
        listing_id: int,
        buyer_name: str,
        crop_name: str,
        score: float
    ) -> Notification:
        """
        Notifies a farmer that a verified buyer has been matched for their crop listing.
        """
        title = f"High Match Buyer Found for {crop_name} ({score}% Fit)"
        title_ur = f"{crop_name} کے لیے خریدار دستیاب ({score}% موزوں)"
        msg = f"Buyer '{buyer_name}' has matched your {crop_name} listing #{listing_id} with an affinity score of {score}%."
        msg_ur = f"خریدار '{buyer_name}' آپ کی فصل {crop_name} خریدنے میں دلچسپی رکھتے ہیں (موزونیت: {score}%)۔"

        return NotificationService.create_notification(
            db=db,
            user_id=farmer_id,
            title=title,
            title_ur=title_ur,
            message=msg,
            message_ur=msg_ur,
            notification_type="BUYER_MATCH",
            data={"listing_id": str(listing_id), "match_score": str(score)}
        )

    @staticmethod
    def notify_deal_update(
        db: Session,
        recipient_user_id: int,
        deal_id: int,
        crop_name: str,
        new_status: str
    ) -> Notification:
        """
        Notifies deal participant about status lifecycle transitions.
        """
        title = f"Deal #{deal_id} Updated: {new_status}"
        title_ur = f"سودا #{deal_id} کی صورتحال: {new_status}"
        msg = f"Status for {crop_name} deal #{deal_id} has progressed to '{new_status}'."
        msg_ur = f"فصل {crop_name} کے سودے #{deal_id} کی نئی صورتحال '{new_status}' ہے۔"

        return NotificationService.create_notification(
            db=db,
            user_id=recipient_user_id,
            title=title,
            title_ur=title_ur,
            message=msg,
            message_ur=msg_ur,
            notification_type="DEAL_STATUS",
            data={"deal_id": str(deal_id), "status": new_status}
        )

    @staticmethod
    def notify_logistics_update(
        db: Session,
        user_id: int,
        request_type: str,
        request_id: int,
        status: str,
        details: str
    ) -> Notification:
        """
        Notifies farmer or buyer about shared transport or cold storage status updates.
        """
        title = f"{request_type} Booking Updated: {status}"
        title_ur = f"{request_type} بکنگ اپ ڈیٹ: {status}"
        msg = f"Your {request_type.lower()} request #{request_id} is now '{status}'. {details}"
        msg_ur = f"آپ کی {request_type} بکنگ #{request_id} اب '{status}' ہے۔ {details}"

        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            title_ur=title_ur,
            message=msg,
            message_ur=msg_ur,
            notification_type="LOGISTICS_UPDATE",
            data={"request_type": request_type, "request_id": str(request_id), "status": status}
        )
