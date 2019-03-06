from datetime import datetime
from pathlib import Path

from crucyble.stages import *
from crucyble.logging import LoggingMeta


class GloVe(metaclass=LoggingMeta):
    """ The GloVe class provides the most flexible interface to the algorithm pipeline.
    Any wrapped types (enums, etc) are defined as the Union of themself and an integer: this class will provide the 
    transformation layer to call the Stage classes, requiring arguments as Enums

    At any layer below this class, primitives are not accepted.

    This class also serves as the singleton for verbosity, logging and other configuration defaults, via class attributes.
    """


    _default_output_path = Path.home() / ".cache" / "crucyble"

    @classmethod
    def output_path_for(cls, filename):
        if not cls._default_output_path.exists():
            cls._default_output_path.mkdir(exist_ok=True)
        return cls._default_output_path / filename
    
    @classmethod
    def vocab_count(cls, corpus, max_vocab: MaxVocab, min_word_count, verbose=None, output_path=None):
        if verbose is None:
            verbose = cls._default_verbosity
        if output_path is None:
            output_path = corpus.parent / "vocab.txt"
        else:
            if not output_path.parent.exists():
                raise ValueError("Directory does not exist for desired output path {}".format(output_path))
        return VocabCount.run(corpus, output_path, max_vocab, min_word_count, verbose=verbose)

    @classmethod
    def cooccur(cls, corpus, vocab,
            symmetry: int, context_window_size: int, memory_limit: float,
            output_path=None, verbose=None, tmp_overflow_file: Path=None):
        if not output_path:
            output_path = cls.output_path_for("cooccur.bin")
        if verbose is None:
            verbose = cls._default_verbosity
        return Cooccur.run(corpus, vocab, output_path, symmetry, context_window_size,
                        memory_limit, verbose=verbose, overflow_file=tmp_overflow_file)
    
    @classmethod
    @with_paths(ignore="output_file")
    def shuffle(cls, cooccur_input, output_file=None, **kwargs):
        return Shuffle.run(cooccur_input, output_file)

    @classmethod
    @with_paths(ignore=['vector_files', 'gradsq_files'])
    def train(cls, cooccur_file, vocab_file, vector_files=None, gradsq_files=None, verbosity=None):
        return Train.run(cooccur_file, vocab_file, vector_files, gradsq_files, verbosity)

    @classmethod
    def from_corpus(cls, *args, **kwargs):
        pass
