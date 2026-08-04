import pytest

from database import Base, engine
from word_service import seed_words


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Seed default words
    seed_words()

    yield