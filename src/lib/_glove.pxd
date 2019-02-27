cdef extern from "glove/glove.h" nogil:
    int train(char* input_file_, char* vocab_file_, char* output_vector_files, char* output_gradsq_files, int verbosity) nogil