import random
from pathlib import Path

from database import SessionLocal
from models import Word


DEFAULT_WORDS = [
    "APPLE",
    "HOUSE",
    "TABLE",
    "PLANT",
    "TRAIN",
    "MOUSE",
    "SNAKE",
    "BRICK",
    "LIGHT",
    "WATER",
    "CLOUD",
    "GRAPE",
    "CHAIR",
    "SMILE",
    "BEACH",
    "PHONE",
    "STONE",
    "HEART",
    "BREAD",
    "RIVER",
]

WORDLIST_PATH = Path(__file__).resolve().parent / "data" / "wordle-list.txt"


def _load_words_from_file():
    if not WORDLIST_PATH.exists():
        return []

    return [
        line.strip().upper()
        for line in WORDLIST_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def seed_words():
    session = SessionLocal()

    try:
        session.query(Word).delete()

        words = _load_words_from_file() or DEFAULT_WORDS
        for word in words:
            session.add(Word(word=word))

        session.commit()

    finally:
        session.close()


def get_all_words():
    words_from_file = _load_words_from_file()
    if words_from_file:
        return words_from_file

    session = SessionLocal()

    try:
        words = session.query(Word).all()

        return [word.word.upper() for word in words]

    finally:
        session.close()


def get_random_word():
    words = get_all_words()

    return random.choice(words)