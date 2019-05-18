# [NLP] Named Entity Recognition

Task for Natural Language Processing course, focusing on the Named Entity Recognition.

[Task description](./9-ner.md)

[Task results](./results.md)

## Running

### Intermediate file preparation (not necessary)
Run `sample_selector.py` to generate input data out of bills into `selected` subdirectory. `cat` it together (`cat * > cat.txt` in its directory) and paste content into a text box at [Clarin NER](http://ws.clarin-pl.eu/ner.shtml), press `Analyse` and wait for results (it may take ages and crash your browser...). Save returned XML file as `output.xml` (there is already one provided).

### Calculations
Run `output_analyzer.py`.

## Requirements
* I assume input files in a directory `ustawy` in a root directory of a repository.
* Required Python libraries are listed in `requirements.txt`.

Tested with Python 3.6.7.