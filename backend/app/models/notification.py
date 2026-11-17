"""
AgriMate AI - Notification Model
FCM Push Notification payloads and persistent in-app notifications.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    title = Column(String(150), nullable=False)
    title_ur = Column(String(200), nullable=True)
    message = Column(Text, nullable=False)
    message_ur = Column(Text, nullable=True)

    # Type: EXPERT_REVIEW, BUYER_MATCH, DEAL_STATUS, LOGISTICS_UPDATE, SYSTEM
    notification_type = Column(String(50), default="SYSTEM", nullable=False)

    data_json = Column(Text, nullable=True)
    fcm_message_id = Column(String(100), nullable=True)
    fcm_dispatched = Column(Boolean, default=False, nullable=False)

    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")

    @property
    def type(self) -> str:
        return self.notification_type

    @property
    def body(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"<Notification id={self.id} user_id={self.user_id} title='{self.title}' read={self.is_read}>"
