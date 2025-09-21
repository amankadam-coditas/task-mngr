from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, index=True)
    # name = Column(String, index=True, nullable=False)
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")       