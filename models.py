from sqlalchemy import Column, Boolean, String, Integer, Text

from database import Base


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, index=True, default="")
    is_done = Column(Boolean, default=False, index=True)
