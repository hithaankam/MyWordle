import random

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


def seed_words():
    session = SessionLocal()

    try:
        session.query(Word).delete()

        for word in DEFAULT_WORDS:
            session.add(Word(word=word))

        session.commit()

    finally:
        session.close()


def get_all_words():
    session = SessionLocal()

    try:
        words = session.query(Word).all()

        return [word.word for word in words]

    finally:
        session.close()


def get_random_word():
    words = get_all_words()

    return random.choice(words)