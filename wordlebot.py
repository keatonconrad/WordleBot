from enum import Enum
import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange
from statistics import mean
from wordfreq import word_frequency
from operator import itemgetter

class LetterResult(Enum):
    GREEN = 0
    YELLOW = 1
    BLACK = 2


with open('all_words.txt', 'r') as f:
    all_words = [line.strip() for line in f.readlines()]


class WordleBot:

    def __init__(self, first_word=None, use_frequencies=True):
        self.all_words = all_words
        self.scores = []
        self.answer = ''
        self.last_score = []
        self.guesses = []
        self.won = False
        self.logging = False
        self.first_word = first_word  # Word to start with
        self.use_frequencies = use_frequencies  # Take into account word frequencies when guessing
        
    
    def play(self):
        self.answer = random.choice(self.all_words)

        while True:
            if len(self.guesses) == 0 and self.first_word:
                guess = self.first_word
            else:
                candidates = self.get_candidates()

                if self.use_frequencies:
                    frequencies = [(word, word_frequency(word, 'en')) for word in candidates]
                    frequencies.sort(key=itemgetter(1), reverse=True)
                    guess = frequencies[0][0]
                else:
                    guess = random.choice(self.all_words)

            score = self.score_guess(guess)

            if all([result[2] == LetterResult.GREEN for result in score]):
                if len(self.guesses) <= 6:
                    self.won = True
                    if self.logging:
                        print('You won!')
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

        if self.logging:
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


class Tester:
    def __init__(self, num_trials=100, first_word=None):
        self.win_counter = 0  # Number of times correct word was guessed within 6 tries
        self.num_guesses = []  # Array of how many tries it took to guess each word
        self.num_trials = num_trials
        self.first_word = first_word

    def play_game(self):
        for i in trange(self.num_trials):
            w = WordleBot(self.first_word)
            w.play()
            self.num_guesses.append(len(w.guesses))
            if w.won:
                self.win_counter += 1

if __name__ == '__main__':
    w = Tester(num_trials=len(all_words))
    w.play_game()
    print(f'% won within 6 guesses: {w.win_counter / w.num_trials}')
    print(f'Average num. guesses: {mean(w.num_guesses)}')
    sns.histplot(data=np.array(w.num_guesses), binrange=(1, max(w.num_guesses)))
    plt.show()