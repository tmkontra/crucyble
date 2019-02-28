cdef extern from "glove/cooccur.h":
    int cooccur(char* corpus_file, char* vocab_file_, char* output_file, int verbosity, 
            int symmetry, int window_size_decl, char* overflow_file, float memory_limit_gb,
            char* log_file)