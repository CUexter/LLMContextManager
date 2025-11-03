"""SQLAlchemy models for chat messages"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime

Base = declarative_base()


class Message(Base):
    """Chat message model with tree structure support"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    speaker = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(String, nullable=False)

    # Self-referential relationship for tree structure
    children = relationship(
        "Message", backref=backref("parent", remote_side=[id]), foreign_keys=[parent_id]
    )

    def __repr__(self):
        return f"<Message(id={self.id}, speaker={self.speaker}, parent_id={self.parent_id})>"

    def get_path_from_root(self, session):
        """Get the full conversation path from root to this message"""
        path = []
        current = self
        while current:
            path.insert(0, current)
            if current.parent_id:
                current = session.query(Message).filter_by(id=current.parent_id).first()
            else:
                current = None
        return path
