# distutils: sources = src/lib/glove/vocab_count.c
# distutils: include_dirs = src/lib/glove

cimport _vocab_count

def vocab_count(char* corpus_file, char* output_file, int verbose, long long max_vocab, long long min_count):
    return _vocab_count.vocab_count(corpus_file, output_file, verbose, max_vocab, min_count)