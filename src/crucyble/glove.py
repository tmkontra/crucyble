from datetime import datetime
from pathlib import Path

from crucyble.stages import *
from crucyble.logging import LoggingMeta

class ModelOutputs:
    def __init__(self, vector_prefix: Path, gradsq_prefix: Path):
        self.vectors = vector_prefix
        self.gradsq = gradsq_prefix

    @staticmethod
    def return_by_type(prefix, file_type):
        if file_type == "txt":
            return prefix.with_suffix(".txt")
        if file_type == "bin":
            return prefix.with_suffix(".bin")

    @property
    def vectors_txt(self):
        return self.return_by_type(self.vectors, "txt")
    
    @property
    def vectors_bin(self):
        return self.return_by_type(self.vectors, "bin")

    @property
    def gradsq_txt(self):
        return self.return_by_type(self.gradsq, "txt")
    
    @property
    def gradsq_bin(self):
        return self.return_by_type(self.gradsq, "bin")


class GloVe(metaclass=LoggingMeta):
    """ The GloVe class provides the most flexible interface to the algorithm pipeline.
    Any wrapped types (enums, etc) are defined as the Union of themself and an integer: this class will provide the 
    transformation layer to call the Stage classes, requiring arguments as Enums

    At any layer below this class, primitives are not accepted.

    This class also serves as the singleton for verbosity, logging and other configuration defaults, via class attributes.
    """

    class DefaultArgs:
        # TODO: add logging to other library sources!
        verbosity = Verbosity.LOW
        # vocab_count
        max_vocab: MaxVocab = VocabCount.MaxVocab(75e3)
        min_word_count: int = 10
        # cooccur
        symmetry: Symmetry = Cooccur.Symmetry.Symmetric
        context_window_size: int = 10
        # train
        num_iteration: int = 25
        model: Model = Train.Model.WORD_NO_BIAS
        use_binary: Output = Train.Output.BOTH
        checkpoint_every = 0
        eta = 0.05
        alpha = 0.75
        x_max = 100

        memory_limit: float = 1.0
        
        @classmethod
        def for_vocab_count(cls, overrides=None):
            return (cls.max_vocab, cls.min_word_count)

        @classmethod
        def for_cooccur(cls, overrides=None):
            return (cls.symmetry, cls.context_window_size, cls.memory_limit)

        @classmethod
        def for_shuffle(cls, overrides=None):
            return
        
        @classmethod
        def for_train(cls, overrides=None):
            args = {
                "num_iteration": cls.num_iteration,
                "model": cls.model,
                "use_binary": cls.use_binary,
                "checkpoint_every": cls.checkpoint_every,
                "eta": cls.eta,
                "alpha": cls.alpha,
                "x_max": cls.x_max
            }
            if overrides:
                args.update((k, overrides[k]) for k in args.keys() & overrides.keys())
            return args


    class DefaultOutputs:
        _default_output_dir = Path.home() / ".cache" / "crucyble"
        vocab_path = _default_output_dir / "vocab.txt"
        cooccur_path = _default_output_dir / "cooccur.bin"
        shuffle_path = _default_output_dir / "cooccur.shuf.bin"
        vectors_path = _default_output_dir / "vectors"
        gradsq_path = _default_output_dir / "gradsq"

    @classmethod
    def default_model_outputs(cls):
        return ModelOutputs(cls.DefaultOutputs.vectors_path, cls.DefaultOutputs.gradsq_path)

    @classmethod
    def output_path_for(cls, filename):
        if not cls._default_output_path.exists():
            cls._default_output_path.mkdir(exist_ok=True)
        return cls._default_output_path / filename
    
    @classmethod
    def vocab_count(cls, corpus, max_vocab: MaxVocab, min_word_count, verbose=None, output_path=None):
        if verbose is None:
            verbose = cls.DefaultArgs.verbosity
        if output_path is None:
            output_path = cls.DefaultOutputs.vocab_path
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
            verbose = cls.DefaultArgs.verbosity
        return Cooccur.run(corpus, vocab, output_path, symmetry, context_window_size,
                        memory_limit, verbose=verbose, overflow_file=tmp_overflow_file)
    
    @classmethod
    @with_paths(ignore="output_file")
    def shuffle(cls, cooccur_input, output_file=None, **kwargs):
        return Shuffle.run(cooccur_input, output_file)

    @classmethod
    @with_paths(ignore=['vector_files', 'gradsq_files'])
    def train(cls, cooccur_file, vocab_file, vector_files=None, gradsq_files=None,
              verbosity=None, num_iteration=None, model=None, use_binary=None, 
              checkpoint_every=None, eta=None, alpha=None, x_max=None):
        return Train.run(cooccur_file, vocab_file, vector_files, gradsq_files, 
                         verbosity, num_iteration, model, use_binary, checkpoint_every,
                         eta, alpha, x_max)

    @classmethod
    def from_corpus(cls, corpus: Path, **overrides):
        cls.vocab_count(corpus, *cls.DefaultArgs.for_vocab_count())
        cls.cooccur(corpus, cls.DefaultOutputs.vocab_path, 1, 10, 4.0, cls.DefaultOutputs.cooccur_path)
        cls.shuffle(cls.DefaultOutputs.cooccur_path, cls.DefaultOutputs.shuffle_path)
        cls.train(cls.DefaultOutputs.shuffle_path, cls.DefaultOutputs.vocab_path, cls.DefaultOutputs.vectors_path, cls.DefaultOutputs.gradsq_path,
                  cls.DefaultArgs.verbosity, **cls.DefaultArgs.for_train(overrides))
        return cls.default_model_outputs()
