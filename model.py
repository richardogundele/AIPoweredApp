from typing import List
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.orm import mapped_column
  
class Base(DeclarativeBase):
    pass

class Chats(Base):
    __tablename__ = "chats"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30))
    prompt: Mapped[Optional[str]] = mapped_column(String(30))
    completion: Mapped[str]  = mapped_column(String(2000))
    
class Emails(Base):
    __tablename__ = "emails"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30))
