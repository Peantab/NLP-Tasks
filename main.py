from elasticsearch import Elasticsearch

es = Elasticsearch()  # By default we connect to localhost:9200


def main():
    prepare_index()
    remove_index()


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
                            "lowercase"
                            # "asciifolding"
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


if __name__ == '__main__':
    main()
