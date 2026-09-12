from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(String, primary_key=True, index=True) # e.g. 'cinderella'
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    category = Column(String, nullable=False) # e.g. 'magic'
    summary = Column(Text, nullable=False)
    reading_time_minutes = Column(Integer, nullable=False)
    emoji = Column(String, nullable=False)
    accent_color = Column(String, nullable=False) # e.g. '0xFF5C6BC0'
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship with story chapters
    chapters = relationship("StoryChapter", back_populates="story", cascade="all, delete-orphan")

class StoryChapter(Base):
    __tablename__ = "story_chapters"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(String, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_number = Column(Integer, default=1, nullable=False)
    title = Column(String, nullable=True) # Chapter title (if exists)
    content = Column(Text, nullable=False) # The text

    story = relationship("Story", back_populates="chapters")