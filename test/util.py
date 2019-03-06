import os
import random

MAX_WORD_COUNT = int(100e3)

def load_words():
    try:
        return _load_unix_dict()
    except EnvironmentError:
        raise RuntimeError("Unable to load sample words! Please submit a github issue.")

def _load_unix_dict():
    try:
        with open('/usr/share/dict/words', "r") as unix_words:
            lines = unix_words.read().splitlines()
        words = lines# random.sample(lines, MAX_WORD_COUNT)
        return words
    except FileNotFoundError:
        raise EnvironmentError