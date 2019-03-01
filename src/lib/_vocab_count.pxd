cdef extern from "glove/vocab_count.h":
    int vocab_count(char* corpus_file, char* output_file, int verbose, long long max_vocab, long long min_count, char* log_file)