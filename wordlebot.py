from enum import Enum
import random

MAX_TRIES = 6

class LetterResult(Enum):
    GREEN = 0
    YELLOW = 1
    BLACK = 2


def get_all_words():
    with open('all_words.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


class WordleBot:

    def __init__(self):
        self.all_words = get_all_words()
        self.scores = []
        self.answer = ''
        self.last_score = []
        self.guesses = []
        self.won = False
        
    
    def play(self):
        self.answer = random.choice(self.all_words)

        for i in range(MAX_TRIES):
            candidates = self.get_candidates()
            guess = random.choice(candidates)
            score = self.score_guess(guess)
            if all([result[2] == LetterResult.GREEN for result in score]):
                print('You won!')
                self.won = True
                break


    def get_candidates(self):
        if len(self.scores) == 0 or all([result[1] == LetterResult.BLACK for result in self.last_score]):
            return self.all_words

        yellow_and_green_letters = set()
        black_letters = set()
        for score in self.scores:
            for letter in score:
                if letter[2] == LetterResult.BLACK:
                    black_letters.add(letter[0])
                else:
                    yellow_and_green_letters.add(letter[0])

        green_tuples = [tup for tup in self.last_score if tup[2] == LetterResult.GREEN]

        candidates = []
        
        for word in self.all_words:
            if all([letter in word for letter in yellow_and_green_letters]) and all([letter not in word for letter in black_letters]):
                if word in self.guesses:
                    continue
                for letter in green_tuples:
                    i = letter[1]
                    if word[i] != letter[0]:
                        break
                else:
                    candidates.append(word)


        return candidates
    
    def score_guess(self, guess):
        self.guesses.append(guess)
        score = []
        for i in range(5):
            if guess[i] == self.answer[i]:
                score.append((guess[i], i, LetterResult.GREEN))
            elif guess[i] in self.answer:
                score.append((guess[i], i, LetterResult.YELLOW))
            else:
                score.append((guess[i], i, LetterResult.BLACK))

        self.print_score(score)
        self.scores.append(score)
        self.last_score = score
        return score

    def print_score(self, score):
        result = []
        for letter in score:
            if letter[2] == LetterResult.GREEN:
                result.append('\x1b[6;30;42m' + letter[0] + '\x1b[0m')
            elif letter[2] == LetterResult.YELLOW:
                result.append('\x1b[6;30;43m' + letter[0] + '\x1b[0m')
            else:
                result.append('\x1b[1;30;40m' + letter[0] + '\x1b[0m')
        print(' '.join(result))


if __name__ == '__main__':
    w = WordleBot()
    w.play()