from abc import ABC, abstractmethod
from enum import Enum
import logging
from functools import partial
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Union

from crucyble import lib
from crucyble.decorators import with_paths, path_to_bytes
from crucyble.logging import logging_callback
from crucyble.verbosity import Verbosity, with_verbosity

class Stage(ABC):
    glove = None # set in __init__.py (i.e. at import time)
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

def log(class_name):
    name = __name__ + "." + class_name
    if Stage.glove.is_logging:
        Stage.logging_callback(logging.getLogger(name), Stage.glove.log_location)

class VocabCount(Stage):
    log = partial(log, "VocabCount")

    @classmethod
    @with_verbosity
    @with_paths(ignore="vocab") # TODO: add check_paths decorator, and passthrough Path objects to lower level classes
    def run(cls, corpus, vocab, max_vocab, min_word_count, verbose=None):
        if verbose is None:
            verbose = cls.glove._default_verbosity
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
        ret = lib.vocab_count.vocab_count(corpus, vocab, 2, max_vocab, min_word_count, cls.glove.log_location_char)
        cls.log()
        return ret 


class Cooccur(Stage):
    log = partial(log, "Cooccur")

    @classmethod
    @with_verbosity
    @with_paths(ignore=["cooccur_output","overflow_file"])
    def run(cls, corpus, vocab, cooccur_output, symmetry, window_size_decl, memory_limit_gb, verbose=None, overflow_file=None):
        if verbose is None:
            verbose = GloVe._default_verbosity
        if overflow_file is None:
            overflow_file = NamedTemporaryFile().name.encode('utf-8')
        if isinstance(symmetry, int):
            symmetry = cls.Symmetry(symmetry)
        symmetry = symmetry.value

        return cls.__cooccur(corpus, vocab, cooccur_output, symmetry, window_size_decl, memory_limit_gb, verbose, overflow_file)

    class Symmetry(Enum):
        Asymmetric = 0
        Symmetric = 1

    @classmethod
    def __cooccur(cls, corpus, vocab, coocur_bin, symmetry: Symmetry, window_size_decl: int, memory_limit_gb: float, verbose, overflow_file):
        ret = lib.cooccur.cooccur(corpus, vocab, coocur_bin, verbose.value, symmetry, window_size_decl, overflow_file, memory_limit_gb, cls.glove.log_location_char)
        cls.log()

        return ret

class Shuffle(Stage):
    log = partial(log, "Shuffle")

    @classmethod
    def run(cls, cooccur_input, output_file, temp_file=None, verbosity=None, requested_memory_limit_gb=None):
        if not temp_file:
            temp_file = NamedTemporaryFile().name.encode('utf-8')
        if not verbosity:
            verbosity = 1
        if not requested_memory_limit_gb:
            requested_memory_limit_gb = 4.0
        cls.__shuffle(cooccur_input, output_file, temp_file, verbosity, requested_memory_limit_gb)
    
    @classmethod
    def __shuffle(cls, cooccurrence_file, output_file, temp_file, verbosity, requested_memory_limit_gb):
        ret = lib.shuffle.shuffle(cooccurrence_file, output_file, temp_file, verbosity, requested_memory_limit_gb, cls.glove.log_location_char)
        cls.log()
        return ret

class Train(Stage):
    log = partial(log, "Train")
    
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

    @classmethod
    @with_verbosity
    def run(cls, cooccurrence_input_file, vocab_file, vector_files_prefix=None, gradsq_files_prefix=None,
            verbosity=None, num_iteration=None, model=None, use_binary=None, checkpoint_every=None,
            eta=None, alpha=None, x_max=None):
        vector_files_prefix = vector_files_prefix or b"vectors"
        gradsq_files_prefix = gradsq_files_prefix or b"gradsq"
        verbosity = verbosity or Verbosity.MEDIUM
        logging.info("saving vectors to: %s", vector_files_prefix)
        logging.info("saving gradsq to %s", gradsq_files_prefix)
        cls.__train(cooccurrence_input_file, vocab_file, vector_files_prefix, gradsq_files_prefix,
                    verbosity.value, num_iteration, model.value, use_binary.value, checkpoint_every, eta, alpha, x_max)

    @classmethod
    def __train(cls, input_matrix, vocab_file, vector_files, gradsq_files, 
                verbosity, num_iteration, model, use_binary, checkpoint_every,
                eta, alpha, x_max):  
        ret = lib.glove.train(input_matrix, vocab_file, vector_files, 1, gradsq_files, verbosity,
                              num_iteration, model, use_binary, checkpoint_every, eta, alpha, x_max,
                              cls.glove.log_location_char)
        cls.log()
        return ret

MaxVocab = Union[VocabCount.MaxVocab, int]
Symmetry = Union[Cooccur.Symmetry, int]
Output = Union[Train.Output, int]
Model = Union[Train.Model, int]