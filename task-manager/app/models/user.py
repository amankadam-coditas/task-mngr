from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.session import Base
from app.core.auth import hash_password, verify_password

class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    email : Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password : Mapped[str] = mapped_column(String(255), nullable=False)
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)
    
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password: str):
        """Set hashed password"""
        self.hashed_password = hash_password(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password"""
        return verify_password(password, self.hashed_password)