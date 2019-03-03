from datetime import datetime
from pathlib import Path

from crucyble.stages import *
from crucyble.decorators import with_paths
from crucyble.logging import LoggingMeta


class GloVe(metaclass=LoggingMeta):
    """ The GloVe class provides the most flexible interface to the algorithm pipeline.
    Any wrapped types (enums, etc) are defined as the Union of themself and an integer: this class will provide the 
    transformation layer to call the Stage classes, requiring arguments as Enums

    At any layer below this class, primitives are not accepted.

    This class also serves as the singleton for verbosity, logging and other configuration defaults, via class attributes.
    """

    # TODO: add logging to other library sources!
    _default_verbosity = Verbosity(1)
    
    @classmethod
    @with_paths(ignore="output_path") # TODO: add check_paths decorator, and passthrough Path objects to lower level classes
    def vocab_count(cls, corpus, max_vocab: MaxVocab, min_word_count, verbose=None, output_path=None):
        if verbose is None:
            verbose = cls._default_verbosity
        if output_path is None:
            output_path = corpus.parent / "vocab.txt"
        return VocabCount.run(corpus, output_path, max_vocab, min_word_count, verbose=verbose)

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
