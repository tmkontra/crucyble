cdef extern from "glove/shuffle.h":
    int shuffle(char* cooccurrence_file, char* output_file, char* temp_file, int verbosity, float memory_limit_gb, char* log_file)