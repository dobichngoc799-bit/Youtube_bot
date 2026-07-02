from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, nullable=False)

    is_active = Column(Boolean, default=True)
    quota_used = Column(Integer, default=0)

    last_used = Column(DateTime, nullable=True)
    last_error = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, unique=True, nullable=False)
    channel_name = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    last_video_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, nullable=False)
    video_id = Column(String, nullable=False)

    sent_at = Column(DateTime, default=datetime.utcnow)
