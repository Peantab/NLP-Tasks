import os
import sys
import regex
from elasticsearch import Elasticsearch

DIRECTORY = '../ustawy'

es = Elasticsearch()  # By default we connect to localhost:9200


def init():
    prepare_index()
    load_data()


def prepare_index():
    request_body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "polish_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "synonym",
                            "morfologik_stem",
                            "lowercase",
                        ]
                    }
                }
            },
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
                "analysis": {
                    "filter": {
                        "synonym": {
                            "type": "synonym",
                            "synonyms": [
                                "kpk => kodeks postępowania karnego",
                                "kpc => kodeks postępowania cywilnego",
                                "kk => kodeks karny",
                                "kc => kodeks cywilny"
                            ]
                        }
                    }
                }
            }
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "bill": {
                        "type": "text",
                        "analyzer": "polish_analyzer"
                    }
                }
            }
        }
    }
    print(es.indices.create(index='law', body=request_body))


def remove_index():
    print(es.indices.delete(index="law"))


def load_data():
    operations = []
    for file in generate_paths():
        bill = file_content(file)
        (year, pos) = year_and_position(file)
        bill_id = generate_id(year, pos)
        operations.append({"create": {"_id": bill_id}})
        operations.append({"bill": bill})
    es.bulk(index="law", doc_type="_doc", body=operations, request_timeout=60)


def generate_paths():
    (_, _, filenames) = next(os.walk(DIRECTORY))
    return map(lambda name: os.path.join(DIRECTORY, name), filenames)


def file_content(path):
    with open(path, 'r') as inp:
        return ''.join(inp.readlines())


def year_and_position(path):
    match = regex.search(DIRECTORY + os.path.sep + r'(?P<year>\d+)_(?P<pos>\d+)\.txt', path)
    return int(match['year']), int(match['pos'])


def generate_id(year, pos):
    return (year % 100) * 10000 + pos


def pretty_print_id(doc_id):
    year = int(doc_id) // 10000
    pos = int(doc_id) % 10000
    return "rok: {:02d}, poz:{:5d}".format(year, pos)


def generate_frequency_lists():
    """
    Use ElasticSearch term vectors API to retrieve and store for each document the following data:
    * The terms (tokens) that are present in the document.
    * The number of times given term is present in the document.
    :return: list of list of frequency
    """
    frequency_lists = []
    for file in generate_paths():
        (year, pos) = year_and_position(file)
        bill_id = generate_id(year, pos)
        tokens = []
        termvectors = es.termvectors(index="law", doc_type="_doc", fields="bill", offsets="false", id=bill_id)
        for term, stats in termvectors["term_vectors"]["bill"]["terms"].items():
            tokens.append((term, stats["term_freq"]))
        frequency_lists.append(tokens)
    return frequency_lists


def aggregate_frequency_lists(frequency_lists):
    """ Aggregate the result to obtain one global frequency list. """
    aggregated = dict()
    for frequency_list in frequency_lists:
        for entry in frequency_list:
            if entry[0] not in aggregated.keys():
                aggregated[entry[0]] = entry[1]
            else:
                aggregated[entry[0]] += entry[1]
    return aggregated


def filter_frequency_list(frequency_list):
    """ Filter the list to keep terms that contain only letters and have at least 2 of them. """
    filtered_frequency_list = []
    correct_term = r"\p{L}{2,}"  # letter of any alphabet, at least 2 of them
    for key, value in frequency_list.items():
        if regex.fullmatch(correct_term, key) is not None:
            filtered_frequency_list.append((key, value))
    return filtered_frequency_list


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stop':
        remove_index()
    elif len(sys.argv) > 1 and sys.argv[1] == 'init':
        init()
    else:
        all_frequency_lists = generate_frequency_lists()
        aggregated = aggregate_frequency_lists(all_frequency_lists)
        filtered = filter_frequency_list(aggregated)
