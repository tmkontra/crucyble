# distutils: sources = src/lib/glove/cooccur.c
# distutils: include_dirs = src/lib/glove

cimport _cooccur

def cooccur(char* corpus_file, char* vocab_file_, char* output_file, int verbosity, 
            int symmetry, int window_size_decl, char* overflow_file, float memory_limit_gb):
    return _cooccur.cooccur(corpus_file, vocab_file_, output_file, verbosity, 
            symmetry, window_size_decl, overflow_file, memory_limit_gb)