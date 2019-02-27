from crucyble import cooccur, vocab_count
print(cooccur)

corpus = b'test/resource/text8'
vocab = b'test/output/vocab.txt'
cooccur_bin = b'test/output/cooccur.bin'
vocab_count.vocab_count(corpus, vocab, 1, 100, 100)
cooccur.cooccur(corpus, vocab, cooccur_bin, 
            2, 1, 15, b'test/output/tmp', 8.0)