"""Database initialization and utilities"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .models import Base, Message


def init_db(db_url="sqlite:///data/chat_history.db"):
    """Initialize database and return session"""
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def create_sample_data(session):
    """Create sample conversation tree for testing"""
    messages = [
        Message(
            id=1,
            parent_id=None,
            speaker="user",
            content="Hello, can you help me with Python?",
        ),
        Message(
            id=2,
            parent_id=1,
            speaker="assistant",
            content="Of course! I'd be happy to help with Python. What specific topic do you need help with?",
        ),
        Message(id=3, parent_id=2, speaker="user", content="How do I read a file?"),
        Message(
            id=4,
            parent_id=3,
            speaker="assistant",
            content='You can use the open() function with a context manager:\n\nwith open("file.txt", "r") as f:\n    content = f.read()',
        ),
        Message(
            id=5,
            parent_id=2,
            speaker="user",
            content="Actually, can you help with lists instead?",
        ),
        Message(
            id=6,
            parent_id=5,
            speaker="assistant",
            content="Sure! Lists in Python are versatile data structures. You can create them with square brackets: my_list = [1, 2, 3]",
        ),
        Message(
            id=7, parent_id=6, speaker="user", content="How do I add items to a list?"
        ),
        Message(
            id=8,
            parent_id=7,
            speaker="assistant",
            content="You can use append() to add items: my_list.append(4), or extend() for multiple items, or insert() for specific positions.",
        ),
    ]

    for msg in messages:
        existing = session.query(Message).filter_by(id=msg.id).first()
        if not existing:
            session.add(msg)

    session.commit()
    return len(messages)
