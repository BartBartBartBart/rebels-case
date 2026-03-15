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
    filename = Column(String, nullable=False, unique=True)
    author = Column(String)
    title = Column(String)
    subject = Column(String)
    keywords = Column(String)
    language = Column(String)
    created = Column(DateTime, default=datetime.datetime.now())
    modified = Column(DateTime, default=datetime.datetime.now())
    file_type = Column(String)
    file_size = Column(Integer)
    paragraph_count = Column(Integer)
    table_count = Column(Integer)
    section_count = Column(Integer)
    word_count = Column(Integer)
    created_with = Column(String)
    label = Column(String, default="unlabeled")  # For classification results

    def __repr__(self):
        return (
            f"<Doc(id={self.id}, "
            f"filename='{self.filename}', "
            f"author='{self.author}', "
            f"title='{self.title}', "
            f"subject='{self.subject}', "
            f"keywords='{self.keywords}'"
            f"language='{self.language}"
            f"created={self.created}, "
            f"modified={self.modified}, "
            f"file_type='{self.file_type}', "
            f"file_size={self.file_size}, "
            f"paragraph_count={self.paragraph_count}, "
            f"table_count={self.table_count}, "
            f"section_count={self.section_count}, "
            f"word_count={self.word_count}, "
            f"created_with='{self.created_with}"
            f"label='{self.label}')>"
        )
