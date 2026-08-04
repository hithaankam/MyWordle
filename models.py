from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String
from database import Base

@dataclass
class Result:
    success: bool
    errors: list[str] = field(default_factory=list)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False
    )