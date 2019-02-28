from datetime import datetime
from enum import Enum
from pathlib import Path

from crucyble import lib
from crucyble.decorators import with_paths
from crucyble.verbosity import Verbosity, with_verbosity

from abc import ABC, abstractmethod

class Stage(ABC):
    @abstractmethod
    def run(self):
        """The entry point for a stage"""


class VocabCount(Stage):

    @classmethod
    @with_verbosity
    def run(cls, corpus, vocab, max_vocab, min_word_count, verbose=None):
        if verbose is None:
            verbose = GloVe._default_verbosity
        return cls.__vocab_count(corpus, vocab, max_vocab, min_word_count, verbose)

    class MaxVocab:
        def __init__(self, limit: int):
            if limit < 0:
                raise ValueError("VocabCount 'max vocab' argument must be integer >= 0")
            self._limit = limit

        @classmethod
        def no_limit(cls):
            return cls(0)

    @staticmethod
    def __vocab_count(corpus, vocab, max_vocab, min_word_count, verbose):
        if isinstance(max_vocab, (int, float)):
            max_vocab = VocabCount.MaxVocab(int(max_vocab))
        vocab_max_length = max_vocab._limit
        return lib.vocab_count.vocab_count(corpus, vocab, verbose.value, vocab_max_length, min_word_count, GloVe.log_location_char)


class Cooccur(Stage):

    @classmethod
    @with_verbosity
    def run(cls, corpus, vocab, coocur_output, symmetry, window_size_decl, memory_limit_gb, verbose=None, overflow_file=None):
        if verbose is None:
            verbose = GloVe._default_verbosity
        return cls.__cooccur(corpus, vocab, coocur_output, symmetry, window_size_decl, memory_limit_gb, verbose, overflow_file)

    class Symmetry(Enum):
        Asymmetric = 0
        Symmetric = 1

    @staticmethod
    def __cooccur(corpus, vocab, coocur_bin, symmetry: Symmetry, window_size_decl: int, memory_limit_gb: float, verbose, overflow_file):
        if isinstance(symmetry, int):
            symmetry = Cooccur.Symmetry(symmetry)
        symmetry = symmetry.value
        return lib.cooccur.cooccur(corpus, vocab, coocur_bin, verbose.value, symmetry, window_size_decl, overflow_file, memory_limit_gb, GloVe.log_location_char)

class Train:
    class Output(Enum):
        TEXT = 0
        BINARY = 1
        BOTH = 2

    class Model(Enum):
        """Text output can include word, context and/ord biases
        """
        ALL = 0
        WORD_NO_BIAS = 1
        WORD_AND_CONTEXT_NO_BIAS = 2
    

class LoggingMeta(type):
    _is_logging = True
    _log_location = Path.home() / ".crucyble" / "{}.log".format(datetime.now().isoformat())

    def no_log(self):
        self._is_logging = False

    @property
    def logging(self):
        return self._is_logging

    @classmethod
    def log_to(cls, log_location: Path):
        cls.log_location = log_location

    @property
    def log_location(self):
        if not self._log_location.parent.exists():
            self._log_location.parent.mkdir(exist_ok=True)
        return self._log_location

    @log_location.setter
    def log_location(self, new_location):
        if not isinstance(new_location, Path):
            raise ValueError("GloVe.log_location must be a valid Path object! Got {} instead.".format(type(new_location)))
        self._log_location = new_location
    
    @property 
    def log_location_char(self):
        return str(self.log_location).encode("utf-8")

class GloVe(metaclass=LoggingMeta):
    # TODO: add logging to other library sources!
    # TODO: add logging callback to surface logfile to python logging interface
    _default_verbosity = Verbosity(1)
    
    @classmethod
    @with_paths() # TODO: add check_paths decorator, and passthrough Path objects to lower level classes
    def vocab_count(cls, corpus, vocab, max_vocab, min_word_count, verbose=None):
        if verbose is None:
            verbose = cls._default_verbosity
        return VocabCount.run(corpus, vocab, max_vocab, min_word_count, verbose=verbose)

    @classmethod
    @with_paths()
    def cooccur(cls, corpus, vocab, cooccur_bin,
            symmetry: int, context_window_size: int,
            memory_limit: float, verbose=None, tmp_overflow_file: Path=None):
        if verbose is None:
            verbose = cls._default_verbosity
        return Cooccur.run(corpus, vocab, cooccur_bin, symmetry, context_window_size,
                        memory_limit, verbose=verbose, overflow_file=tmp_overflow_file)

    @classmethod
    def from_corpus(cls, *args, **kwargs):
        pass
