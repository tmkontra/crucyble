//  Tool to shuffle entries of word-word cooccurrence files
//
//  Copyright (c) 2014 The Board of Trustees of
//  The Leland Stanford Junior University. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//
//
//  For more information, bug reports, fixes, contact:
//    Jeffrey Pennington (jpennin@stanford.edu)
//    GlobalVectors@googlegroups.com
//    http://nlp.stanford.edu/projects/glove/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <shuffle.h>

#define MAX_STRING_LENGTH 1000

static const long LRAND_MAX = ((long) RAND_MAX + 2) * (long)RAND_MAX;
typedef double real;

typedef struct cooccur_rec {
    int word1;
    int word2;
    real val;
} CREC;

int verbose = 2; // 0, 1, or 2
long long array_size = 2000000; // size of chunks to shuffle individually
char *file_head; // temporary file string
real memory_limit = 2.0; // soft limit, in gigabytes

/* Efficient string comparison */
int scmp( char *s1, char *s2 ) {
    while(*s1 != '\0' && *s1 == *s2) {s1++; s2++;}
    return(*s1 - *s2);
}


/* Generate uniformly distributed random long ints */
static long rand_long(long n) {
    long limit = LRAND_MAX - LRAND_MAX % n;
    long rnd;
    do {
        rnd = ((long)RAND_MAX + 1) * (long)rand() + (long)rand();
    } while (rnd >= limit);
    return rnd % n;
}

/* Write contents of array to binary file */
int write_chunk(CREC *array, long size, FILE *fout) {
    long i = 0;
    for(i = 0; i < size; i++) fwrite(&array[i], sizeof(CREC), 1, fout);
    return 0;
}

/* Fisher-Yates shuffle */
void fyshuffle(CREC *array, long n) {
    long i, j;
    CREC tmp;
    for (i = n - 1; i > 0; i--) {
        j = rand_long(i + 1);
        tmp = array[j];
        array[j] = array[i];
        array[i] = tmp;
    }
}

/* Merge shuffled temporary files; doesn't necessarily produce a perfect shuffle, but good enough */
int shuffle_merge(int num, char* output_file) {
    long i, j, k, l = 0;
    int fidcounter = 0;
    CREC *array;
    char filename[MAX_STRING_LENGTH];
    FILE **fid, *fout = fopen(output_file, "wb");
    
    array = malloc(sizeof(CREC) * array_size);
    fid = malloc(sizeof(FILE) * num);
    for(fidcounter = 0; fidcounter < num; fidcounter++) { //num = number of temporary files to merge
        sprintf(filename,"%s_%04d.bin",file_head, fidcounter);
        fid[fidcounter] = fopen(filename, "rb");
        if(fid[fidcounter] == NULL) {
            fprintf(stderr, "Unable to open file %s.\n",filename);
            return 1;
        }
    }
    if(verbose > 0) fprintf(stderr, "Merging temp files: processed %ld lines.", l);
    
    while(1) { //Loop until EOF in all files
        i = 0;
        //Read at most array_size values into array, roughly array_size/num from each temp file
        for(j = 0; j < num; j++) {
            if(feof(fid[j])) continue;
            for(k = 0; k < array_size / num; k++){
                fread(&array[i], sizeof(CREC), 1, fid[j]);
                if(feof(fid[j])) break;
                i++;
            }
        }
        if(i == 0) break;
        l += i;
        fyshuffle(array, i-1); // Shuffles lines between temp files
        write_chunk(array,i,fout);
        if(verbose > 0) fprintf(stderr, "\033[31G%ld lines.", l);
    }
    fprintf(stderr, "\033[0GMerging temp files: processed %ld lines.", l);
    for(fidcounter = 0; fidcounter < num; fidcounter++) {
        fclose(fid[fidcounter]);
        sprintf(filename,"%s_%04d.bin",file_head, fidcounter);
        remove(filename);
    }
    fprintf(stderr, "\n\n");
    free(array);
    fclose(fout);
    return 0;
}

/* Shuffle large input stream by splitting into chunks */
int shuffle_by_chunks(char* input_file, char* output_file) {
    long i = 0, l = 0;
    int fidcounter = 0;
    char filename[MAX_STRING_LENGTH];
    CREC *array;
    FILE *fin = fopen(input_file, "rb"), *fid;
    array = malloc(sizeof(CREC) * array_size);
    
    fprintf(stderr,"SHUFFLING COOCCURRENCES\n");
    if(verbose > 0) fprintf(stderr,"array size: %lld\n", array_size);
    sprintf(filename,"%s_%04d.bin",file_head, fidcounter);
    fid = fopen(filename,"w");
    if(fid == NULL) {
        fprintf(stderr, "Unable to open file %s.\n",filename);
        return 1;
    }
    if(verbose > 1) fprintf(stderr, "Shuffling by chunks: processed 0 lines.");
    
    while(1) { //Continue until EOF
        if(i >= array_size) {// If array is full, shuffle it and save to temporary file
            fyshuffle(array, i-2);
            l += i;
            if(verbose > 1) fprintf(stderr, "\033[22Gprocessed %ld lines.", l);
            write_chunk(array,i,fid);
            fclose(fid);
            fidcounter++;
            sprintf(filename,"%s_%04d.bin",file_head, fidcounter);
            fid = fopen(filename,"w");
            if(fid == NULL) {
                fprintf(stderr, "Unable to open file %s.\n",filename);
                return 1;
            }
            i = 0;
        }
        fread(&array[i], sizeof(CREC), 1, fin);
        if(feof(fin)) break;
        i++;
    }
    fclose(fin);
    fyshuffle(array, i-1); //Last chunk may be smaller than array_size
    write_chunk(array,i,fid);
    l += i;
    if(verbose > 1) fprintf(stderr, "\033[22Gprocessed %ld lines.\n", l);
    if(verbose > 1) fprintf(stderr, "Wrote %d temporary file(s).\n", fidcounter + 1);
    fclose(fid);
    free(array);
    return shuffle_merge(fidcounter + 1, output_file); // Merge and shuffle together temporary files
}

int shuffle(char* cooccurrence_file, char* output_file, char* temp_file, int verbosity, float memory_limit_gb) {
    file_head = malloc(sizeof(char) * MAX_STRING_LENGTH);
    verbose = verbosity;
    file_head = temp_file;
    memory_limit = memory_limit_gb;
    // TODO: investigate SIGSEGV when memory > 2.0
    array_size = (long long) (0.80 * (real)memory_limit * 1073741824/(sizeof(CREC)));
    // TODO: add back in array_size override
    return shuffle_by_chunks(cooccurrence_file, output_file);
}

