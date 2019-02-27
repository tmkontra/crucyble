# distutils: sources = src/lib/glove/vocab_count.c
# distutils: include_dirs = src/lib/glove

cimport cglove

def vocab_count(char* corpus, char* output, int arg, long long arg2, long long arg3):
    return cglove.vocab_count(corpus, output, arg, arg2, arg3)
