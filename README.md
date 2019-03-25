# [NLP] ElasticSearch

Task for Natural Language Processing course, focusing on the use of ElasticSearch.

[Task description](./2-fts.md).

[Task results](./results.md)

## Running
 * Run ElasticSearch,
 * Run `runall.sh`
 
 OR:
 
 * Run ElasticSearch,
 * Run `python main.py init` to load data to an index,
 * Run `python main.py`,
 * Run `python main.py stop` to remove index from ElasticSearch.

## Requirements
I assume input files in subdirectory `ustawy`.
Required Python libraries are listed in `requirements.txt`.
Required ES plugin:
`pl.allegro.tech.elasticsearch.plugin:elasticsearch-analysis-morfologik:6.6.2` 

Tested with Python 3.6.7, ElasticSearch 6.6.2