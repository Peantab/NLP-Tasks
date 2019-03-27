# [NLP] Levenshtein distance

Task for Natural Language Processing course.

[Task description](./3-levenshtein.md)

[Task results](./results.md)

## Running
 * run ElasticSearch,
 * run `runall.sh`. Results will be generated as `results.md`
 
 OR:
 
 * run ElasticSearch,
 * run `python main.py init` to load data to an index,
 * run `python main.py`, which will display text results on standard output and save a chart into `plot.png`,
 * run `python main.py stop` to remove index from ElasticSearch.

## Requirements
I assume input files in a directory `ustawy` as well as `polimorfologik-2.1.txt` dictionary file in a root directory of a repository.
Required Python libraries are listed in `requirements.txt`.
Required ES plugin:
`pl.allegro.tech.elasticsearch.plugin:elasticsearch-analysis-morfologik:6.6.2` 

Tested with Python 3.6.7, ElasticSearch 6.6.2