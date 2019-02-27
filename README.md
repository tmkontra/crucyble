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

The bulk of the alterations consist of removing the `main()` methods from the glove applications, and converting them to accept filenames instead of stdin/stdout. (See pull requests [1](https://github.com/ttymck/crucyble/pull/1), [2](https://github.com/ttymck/crucyble/pull/2), and [3](https://github.com/ttymck/crucyble/pull/3))

These altered C sources are then wrapped with Cython to provide "native extensions" in the Python runtime.

## Development

### Local Testing
To test this library locally:
1. clone the repo
2. from `crucyble/` run `python setup.py build_ext -i`
3. try: `python test/test_glove.py`
4. examine the outputs!

You can change the corpus variable in `test_glove.py` to point to any corpus you have locally.

### Contributing
...coming soon

## Performance

Todo... :shrug:

## License Info

Derivative implementation of the [GloVe library from Stanford](https://github.com/stanfordnlp/GloVe) redistributed in accordance with [Apache License](./src/lib/glove/LICENSE) and redistributed under [MIT License](./LICENSE)