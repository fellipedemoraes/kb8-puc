

class WrongAttempt(Exception):
    pass


class Guess:
    def __init__(self, word):
        self.word = word

    def attempt(self, guess):
        if len(guess) < len(self.word):
            raise WrongAttempt("Incorrect. Guess is too short")
        if len(guess) > len(self.word):
            raise WrongAttempt("Incorrect. Guess is too long")

        correct, wrong = self.compare_strings(guess)
        if correct == len(self.word):
            return True
        else:
            raise WrongAttempt(
                (f"Incorrect, but you gessed "
                 f"{correct} {plural('letter', correct)} in correct {plural('position', correct)}, "
                 f"{wrong} in wrong {plural('position', wrong)}, "
                 f"of {len(self.word)} {plural('letter', len(self.word))}"))

    def compare_strings(self, guess):
        target = self.word
        if len(target) != len(guess):
            raise WrongAttempt(
                "Incorrect. Both strings must be of the same length.")

        correct_letters = 0
        correct_positions = 0

        # Create a list to store if a letter has already been counted for correct letter
        target_letter_counted = [False] * len(target)

        # First, count letters in the correct position
        for i in range(len(target)):
            if guess[i] == target[i]:
                correct_positions += 1
                target_letter_counted[i] = True

        # Now, count letters that are correct but in the wrong position
        for i in range(len(guess)):
            if guess[i] != target[i]:  # Skip already matched letters
                for j in range(len(target)):
                    if guess[i] == target[j] and not target_letter_counted[j]:
                        correct_letters += 1
                        target_letter_counted[j] = True
                        break

        return correct_positions, correct_letters


def plural(word, count):
    return word if count == 1 else word + "s"
