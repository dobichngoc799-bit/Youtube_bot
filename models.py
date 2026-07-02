from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, nullable=False)

    is_active = Column(Boolean, default=True)
    quota_used = Column(Integer, default=0)
    rotation_index = Column(Integer, default=0)

    last_used = Column(DateTime, nullable=True)
    last_error = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)

    channel_id = Column(String, unique=True, nullable=False, index=True)
    channel_name = Column(String, nullable=False)

    handle = Column(String, unique=True, nullable=True)

    upload_playlist = Column(String, nullable=False)

    thumbnail = Column(String, nullable=True)

    subscriber_count = Column(Integer, default=0)
    video_count = Column(Integer, default=0)

    last_video_id = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    channel_id = Column(String, nullable=False, index=True)
    video_id = Column(String, nullable=False, index=True)

    sent_at = Column(DateTime, default=datetime.utcnow)