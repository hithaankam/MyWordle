from word_service import (
    seed_words,
    get_all_words,
    get_random_word
)


def test_database_contains_twenty_words():
    seed_words()

    words = get_all_words()

    assert len(words) == 20


def test_all_words_are_uppercase():
    seed_words()

    words = get_all_words()

    assert all(word.isupper() for word in words)


def test_all_words_are_five_letters():
    seed_words()

    words = get_all_words()

    assert all(len(word) == 5 for word in words)


def test_no_duplicate_words():
    seed_words()

    words = get_all_words()

    assert len(words) == len(set(words))


def test_random_word_exists_in_database():
    seed_words()

    words = get_all_words()

    random_word = get_random_word()

    assert random_word in words