from sqlalchemy import  String, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.session import Base
from typing import Optional
from app.models.enums import TaskPriority

class Task(Base):
    __tablename__ = "tasks"

    # id = Column(Integer, primary_key=True, index=True)
    # title = Column(String, index=True, nullable=False)
    # description = Column(String, nullable=True)
    # status = Column(String, default="pending")
    # priority = Column(Enum(TaskPriority), default=TaskPriority.LOW, nullable=False)
    # user_id = Column(Integer, ForeignKey("users.id"))
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending")
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), default=TaskPriority.LOW, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")