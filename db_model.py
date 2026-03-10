from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime


class Doc(Base):
    """
    A SQLAlchemy model to represent document metadata in the database.
    Each document has an ID, title, content, and a timestamp for
    when it was created.
    """

    __tablename__ = "docs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_type = Column(String)
    file_size = Column(Integer)
    label = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return (
            f"<Doc(id={self.id}, "
            f"filename='{self.filename}', "
            f"timestamp='{self.timestamp}')>"
        )
