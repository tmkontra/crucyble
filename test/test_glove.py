from pathlib import Path

from crucyble import GloVe

test_dir = Path(__file__).parent

corpus = test_dir / 'resource/text8'
vocab =  test_dir / 'output/vocab.txt'
cooccur_bin = test_dir / 'output/cooccur.bin'
shuf_bin = test_dir / 'output/cooccur.shuf.bin'
vectors = test_dir / 'output/vectors'
gradsq = test_dir / 'output/gradsq'

GloVe.log_location = GloVe.log_location.parent / "test.log"
GloVe.no_log()

maxvocab = 100e2
min_count = 10 
GloVe.vocab_count(corpus, maxvocab, min_count, output_path=vocab)
overflow_file = test_dir / 'tmp'
GloVe.cooccur(corpus, vocab, cooccur_bin, 1, 15, 8.0, tmp_overflow_file=overflow_file)
# shuffle.shuffle(cooccur_bin, shuf_bin, b'test/output/shuf', 2, 2.2)
# glove.train(shuf_bin, vocab, vectors, gradsq, 2)