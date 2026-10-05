import uuid
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from sqlalchemy.dialects.postgresql import JSONB
from app.database.database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    hero = Column(String, nullable=False)
    setting = Column(String, nullable=False)
    style = Column(String, nullable=False)
    generated_chapters_count = Column(Integer, default=0, nullable=False)
    category = Column(String, nullable=False)
    full_story_context = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    short_story_context = Column(String, nullable=False)
    reading_time_minutes = Column(Integer, nullable=False)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with user
    owner = relationship("User", back_populates="stories")
    # Relationship with story chapters
    chapters = relationship("StoryChapter", back_populates="story", cascade="all, delete-orphan")

class StoryChapter(Base):
    __tablename__ = "story_chapters"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(String, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_number = Column(Integer, default=1, nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    chapter_description = Column(Text, nullable=False)
    next_options = Column(
        JSONB,
        nullable=False,
        server_default=text("'[]'::jsonb"),
    )

    # Relationship with story
    story = relationship("Story", back_populates="chapters")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    google_sub = Column(String, unique=True, index=True, nullable=True)

    subscription_credits = Column(Integer, default=5)
    purchased_credits = Column(Integer, default=0)
    subscription_tier = Column(String, default="free")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship with story
    stories = relationship(
        "Story", back_populates="owner", cascade="all, delete-orphan"
    )

class StorySettings(Base):
    __tablename__ = "story_settings"

    id = Column(Integer, primary_key=True, index=True)
    catalog = Column(JSONB, nullable=False)