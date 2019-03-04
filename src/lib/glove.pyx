# distutils: sources = src/lib/glove/glove.c
# distutils: include_dirs = src/lib/glove

cimport _glove

def train(char* input_file_, char* vocab_file_, char* output_vector_files, int do_save_gradsq_files, char* opt_output_gradsq_files, int verbosity):
    _glove.train(input_file_, vocab_file_, output_vector_files, do_save_gradsq_files, opt_output_gradsq_files, verbosity)