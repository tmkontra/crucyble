from abc import ABC, abstractmethod
from enum import Enum
import logging
from functools import partial

from crucyble import lib
from crucyble.logging import logging_callback
from crucyble.types import EnumUnion
from crucyble.verbosity import Verbosity, with_verbosity

class Stage(ABC):
    logging_callback = logging_callback
    """A single unit of work for the GloVe pipeline.
    These class provide methods that transform arguments to the corresponding C types.
    
    A stage must employ enum arguments, it will not transform integer values like the GloVe class.
    A stage must have a private __stage_name method that cannot have any optional arguments, to properly respect
    all arguments being required by the C extensions.
    """

    @abstractmethod
    def run(self):
        """The entry point for a stage"""

def log(name):
    if Stage.glove.is_logging:
        Stage.logging_callback(logging.getLogger(name), Stage.glove.log_location)

class VocabCount(Stage):
    log = partial(log, __name__+".VocabCount")

    @classmethod
    @with_verbosity
    def run(cls, corpus, vocab, max_vocab, min_word_count, verbose=None):
        if verbose is None:
            verbose = GloVe._default_verbosity
        return cls.__vocab_count(corpus, vocab, max_vocab, min_word_count, verbose)

    class MaxVocab(int):
        def __new__(cls, value, *args, **kwargs):
            if value < 0:
                raise ValueError("VocabCount 'max vocab' argument must be a positive integer")
            return  super(cls, cls).__new__(cls, value)

        @classmethod
        def no_limit(cls):
            return cls(0)

    @classmethod
    def __vocab_count(cls, corpus, vocab, max_vocab, min_word_count, verbose):
        if isinstance(max_vocab, (int, float)):
            max_vocab = cls.MaxVocab(int(max_vocab))
        ret = lib.vocab_count.vocab_count(corpus, vocab, verbose.value, max_vocab, min_word_count, cls.glove.log_location_char)
        cls.log()
        return ret 


class Cooccur(Stage):
    log = partial(log, __name__+".Cooccur")

    @classmethod
    @with_verbosity
    def run(cls, corpus, vocab, coocur_output, symmetry, window_size_decl, memory_limit_gb, verbose=None, overflow_file=None):
        if verbose is None:
            verbose = GloVe._default_verbosity
        return cls.__cooccur(corpus, vocab, coocur_output, symmetry, window_size_decl, memory_limit_gb, verbose, overflow_file)

    class Symmetry(Enum):
        Asymmetric = 0
        Symmetric = 1

    @classmethod
    def __cooccur(cls, corpus, vocab, coocur_bin, symmetry: Symmetry, window_size_decl: int, memory_limit_gb: float, verbose, overflow_file):
        if isinstance(symmetry, int):
            symmetry = cls.Symmetry(symmetry)
        symmetry = symmetry.value
        ret = lib.cooccur.cooccur(corpus, vocab, coocur_bin, verbose.value, symmetry, window_size_decl, overflow_file, memory_limit_gb, cls.glove.log_location_char)
        cls.log()
        return ret

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

MaxVocab = EnumUnion(VocabCount.MaxVocab)
Symmetry = EnumUnion(Cooccur.Symmetry)
Output = EnumUnion(Train.Output)
Model = EnumUnion(Train.Model)