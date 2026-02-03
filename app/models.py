import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True)
    creator_id = Column(String, nullable=False)
    video_created_at = Column(DateTime(timezone=True), nullable=False)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    reports_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    snapshots = relationship("VideoSnapshot", back_populates="video")



class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id = Column(String, primary_key=True)  # uuid
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    reports_count = Column(Integer, default=0)

    delta_views_count = Column(Integer, default=0)
    delta_likes_count = Column(Integer, default=0)
    delta_comments_count = Column(Integer, default=0)
    delta_reports_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    video = relationship("Video", back_populates="snapshots")