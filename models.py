from dataclasses import dataclass, field
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base

@dataclass
class Result:
    success: bool
    errors: list[str] = field(default_factory=list)
    game_id: int | None = None
    colors: list | None = None
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

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)

    word = Column(String(5), unique=True, nullable=False)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    word_id = Column(
        Integer,
        ForeignKey("words.id"),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )

    guesses_used = Column(
        Integer,
        nullable=False,
        default=0
    )

    started_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now
    )

class Guess(Base):
    __tablename__ = "guesses"

    id = Column(Integer, primary_key=True)

    game_id = Column(
        Integer,
        ForeignKey("games.id"),
        nullable=False
    )

    guess_number = Column(
        Integer,
        nullable=False
    )

    guessed_word = Column(
        String(5),
        nullable=False
    )

    submitted_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now
    )