# distutils: sources = src/lib/glove/shuffle.c
# distutils: include_dirs = src/lib/glove

cimport _shuffle

def shuffle(char* cooccurrence_file, char* output_file, char* temp_file, int verbosity, float memory_limit_gb, char* log_file):
    return _shuffle.shuffle(cooccurrence_file, output_file, temp_file, verbosity, memory_limit_gb, log_file)