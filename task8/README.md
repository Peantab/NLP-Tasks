# [NLP] Text classification

Task for Natural Language Processing course, focusing on the text classification.

[Task description](./8-classification.md)

[Task results](./results.md)

## Running
Run `file_preparator.py` to generate input data out of bills. Scripts `classification_*.py` are training and testing particular models (for *fastText* testing isn't a part of a script, details in [results](./results.md)).

## Requirements
* I assume input files in a directory `ustawy` in a root directory of a repository.
* Download *fastText v0.2.0*, extract here and install Python package as in `fastText-0.2.0/python/README.md`.
* Required Python libraries are listed in `requirements.txt`.