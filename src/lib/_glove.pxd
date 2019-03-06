cdef extern from "glove/glove.h" nogil:
    int train(char* input_file_, char* vocab_file_, char* output_vector_files, 
          int do_save_gradsq_files, char* opt_output_gradsq_files, int verbosity,
          int num_iteration, int model, int use_binary, int checkpoint_every, 
          double eta, double alpha, double x_max,
          char *log_file) nogil