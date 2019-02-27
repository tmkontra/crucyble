# crucyble

A **Cy**thon Wrapped GloVe (Global Vectors for Word Representation)

> *crucible*, noun. 
>
> **Pronounciation**: \ ˈkrü-sə-bəl \
> 1. a vessel of a very refractory material used for melting...
> 2. a severe test
> 3. a vessel of a very refractory (see refractory entry 1 sense 3) material (such as porcelain) used for melting and calcining a substance that requires a   high degree of heat
>
> **Synonyms**: gauntlet, ...

## Overview

This library aims to provide the GloVe algorithm in a nearly-unaltered format relative to its original distribution by stanfordnlp.

The bulk of the alterations consist of removing the `main()` methods from the glove applications, and converting them to accept filenames instead of stdin/stdout.

These altered C sources are then wrapped with Cython to provide "native extensions" in the Python runtime.

## Performance

Todo... :shrug:

## License Info

Derivative implementation of the [GloVe library from Stanford](https://github.com/stanfordnlp/GloVe) redistributed in accordance with [Apache License](./src/lib/glove/LICENSE) and redistributed under [MIT License](./LICENSE)