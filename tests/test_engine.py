from game_engine import WordleEngine, LetterState


def test_correct_guess():
    engine = WordleEngine("APPLE")

    result = engine.submit_guess("APPLE")

    assert engine.is_won()

    assert result == [
        LetterState.CORRECT,
        LetterState.CORRECT,
        LetterState.CORRECT,
        LetterState.CORRECT,
        LetterState.CORRECT,
    ]


def test_wrong_position():
    engine = WordleEngine("APPLE")

    result = engine.submit_guess("PLEAP")

    assert LetterState.PRESENT in result


def test_absent_letter():
    engine = WordleEngine("APPLE")

    result = engine.submit_guess("ZZZZZ")

    assert result == [
        LetterState.ABSENT,
        LetterState.ABSENT,
        LetterState.ABSENT,
        LetterState.ABSENT,
        LetterState.ABSENT,
    ]


def test_duplicate_letters():
    engine = WordleEngine("APPLE")

    result = engine.submit_guess("PPPPP")

    assert result.count(LetterState.CORRECT) == 2
    assert result.count(LetterState.ABSENT) == 3


def test_loss_after_five_attempts():
    engine = WordleEngine("APPLE")

    for _ in range(5):
        engine.submit_guess("ZZZZZ")

    assert engine.is_lost()


def test_cannot_guess_after_game_over():
    engine = WordleEngine("APPLE")

    for _ in range(5):
        engine.submit_guess("ZZZZZ")

    try:
        engine.submit_guess("APPLE")
        assert False
    except ValueError:
        assert True