import os
import sys
import re
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
                            "morfologik_stem",
                            "lowercase",
                            "synonym"
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
    for file in generate_paths():
        bill = file_content(file)
        (year, pos) = year_and_position(file)
        bill_id = (year % 100) * 10000 + pos
        json = {"bill": bill}
        es.create(index="law", doc_type="_doc", id=bill_id, body=json)


def generate_paths():
    (_, _, filenames) = next(os.walk(DIRECTORY))
    return map(lambda name: os.path.join(DIRECTORY, name), filenames)


def file_content(path):
    with open(path, 'r') as inp:
        return ''.join(inp.readlines())


def year_and_position(path):
    match = re.search(DIRECTORY + os.path.sep + r'(?P<year>\d+)_(?P<pos>\d+)\.txt', path)
    return int(match['year']), int(match['pos'])


def pretty_print_id(doc_id):
    year = int(doc_id) // 10000
    pos = int(doc_id) % 10000
    return "rok: {:02d}, poz:{:5d}".format(year, pos)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stop':
        remove_index()
    elif len(sys.argv) > 1 and sys.argv[1] == 'init':
        init()
    else:
        pass
