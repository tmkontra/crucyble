cdef extern from "glove/glove.h" nogil:
    int train(char* input_file_, char* vocab_file_, char* output_vector_files, int do_save_gradsq_files, char* opt_output_gradsq_files, int verbosity) nogil