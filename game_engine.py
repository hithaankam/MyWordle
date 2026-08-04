from enum import Enum


class LetterState(Enum):
    CORRECT = "GREEN"
    PRESENT = "ORANGE"
    ABSENT = "GREY"


class WordleEngine:
    MAX_ATTEMPTS = 5

    def __init__(self, secret_word):
        self.secret_word = secret_word
        self.attempts = 0
        self.won = False

    def submit_guess(self, guess):
        if self.is_game_over():
            raise ValueError("Game is already over.")

        if len(guess) != 5:
            raise ValueError("Guess must contain exactly 5 letters.")

        if not guess.isalpha():
            raise ValueError("Guess must contain only alphabetic letters.")

        if guess != guess.upper():
            raise ValueError("Guess must be uppercase.")

        self.attempts += 1

        result = self._evaluate_guess(guess)

        if guess == self.secret_word:
            self.won = True

        return result

    def is_won(self):
        return self.won

    def is_lost(self):
        return (not self.won) and self.attempts >= self.MAX_ATTEMPTS

    def is_game_over(self):
        return self.is_won() or self.is_lost()

    def _evaluate_guess(self, guess):
        result = [None] * 5
        remaining = list(self.secret_word)

        # Green pass
        for i in range(5):
            if guess[i] == self.secret_word[i]:
                result[i] = LetterState.CORRECT
                remaining[i] = None

        # Orange/Grey pass
        for i in range(5):
            if result[i] is not None:
                continue

            if guess[i] in remaining:
                result[i] = LetterState.PRESENT
                remaining[remaining.index(guess[i])] = None
            else:
                result[i] = LetterState.ABSENT

        return result