from pathlib import Path
import random
import shutil

import pytest

from crucyble import GloVe
try:
    from util import load_words
except ImportError:
    from .util import load_words


test_dir = Path(__file__).parent / "pytest"
test_dir.mkdir(exist_ok=True)
GloVe.log_location = GloVe.log_location.parent / "test.log"
# GloVe.no_log()

class TestGlove:
    CORPUS_WORD_COUNT = int(1e6)

    @classmethod
    def setup_class(cls):
        """ create output location and input corpus
        """
        words = load_words()
        cls.Paths.corpus.parent.mkdir(exist_ok=True)
        with open(cls.Paths.corpus, "w") as f:
            for i in range(cls.CORPUS_WORD_COUNT):
                f.write("{} ".format(random.choice(words)))
        try:
            cls.Paths.test_output_dir.mkdir(exist_ok=False)
        except FileExistsError:
            shutil.rmtree(cls.Paths.test_output_dir)
            cls.Paths.test_output_dir.mkdir()

    @classmethod
    def teardown_class(cls):
        """ delete all files created during tests
        """
        # shutil.rmtree(cls.Paths.test_output_dir)

    class Paths:
        corpus = test_dir / 'input/corpus.txt'
        # corpus = test_dir.parent / "resource/text8"
        test_output_dir = test_dir / "output"
        vocab =  test_output_dir / 'vocab.txt'
        cooccur_bin = test_output_dir / 'cooccur.bin'
        shuf_bin = test_output_dir / 'cooccur.shuf.bin'
        vectors_prefix = test_output_dir / 'vectors'
        gradsq_prefix = test_output_dir / 'gradsq'

    def test_vocab_count(self):
        maxvocab = 25e3
        min_count = 5
        GloVe.vocab_count(self.Paths.corpus, maxvocab, min_count, output_path=self.Paths.vocab)
        assert(self.Paths.vocab.exists())

    def test_cooccur(self):
        symmetry = GloVe.DefaultArgs.symmetry
        verbosity = GloVe.DefaultArgs.verbosity
        context_window_size = 10
        memory_limit_gb = 8.0
        GloVe.cooccur(self.Paths.corpus, self.Paths.vocab, symmetry, context_window_size, memory_limit_gb,
                    output_path=self.Paths.cooccur_bin, verbose=verbosity)
        assert(self.Paths.cooccur_bin.exists())

    def test_shuffle(self):
        GloVe.shuffle(self.Paths.cooccur_bin, output_file=self.Paths.shuf_bin)#, shuf_bin, b'test/output/shuf', 2, 2.2)
        assert(self.Paths.shuf_bin.exists())

    def test_train(self):
        verbosity = GloVe.DefaultArgs.verbosity
        GloVe.train(self.Paths.shuf_bin, self.Paths.vocab, vector_files=self.Paths.vectors_prefix, gradsq_files=self.Paths.gradsq_prefix,
         verbosity=verbosity, **GloVe.DefaultArgs.for_train({"num_iteration":3}))
        assert(self.Paths.vectors_prefix.with_suffix(".txt").exists())
        assert(self.Paths.gradsq_prefix.with_suffix(".txt").exists())

    def test_from_corpus(self):
        result = GloVe.from_corpus(self.Paths.corpus, num_iteration=3)
        assert(result.vectors_txt.exists())
        assert(result.gradsq_txt.exists())