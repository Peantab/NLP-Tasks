import os
import sys
import regex
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import Levenshtein

DIRECTORY = '../ustawy'
DICTIONARY = '../polimorfologik-2.1.txt'

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


def generate_plot(frequency_list):
    """
    Make a plot in a logarithmic scale:
    * X-axis should contain the rank of a term, meaning the first rank belongs to the term with the highest number
      of occurrences; the terms with the same number of occurrences should be ordered by their name,
    * Y-axis should contain the number of occurrences of the term with given rank.
    """
    frequency_list.sort(key=lambda e: e[0])  # alphabetically
    frequency_list.sort(key=lambda e: e[1], reverse=True)  # by number of occurrences
    x = range(len(frequency_list))
    y = [entry[1] for entry in frequency_list]
    plt.semilogy(x, y)
    plt.title('Terms Frequency')
    plt.grid(True)
    plt.savefig("plot.png")


def unknown_words(frequency_list, dictionary):
    """ Download polimorfologik.zip dictionary and use it to find all words that do not appear in that dictionary. """
    unknown = []
    for entry in frequency_list:
        key = entry[0]
        if key not in dictionary:
            unknown.append(entry)
    return unknown


def load_dictionary():
    result_dictionary = set()
    with open(DICTIONARY, "r") as dictionary_file:
        for line in dictionary_file.readlines():
            result_dictionary.add(line.split(sep=";", maxsplit=1)[0].lower())
    return result_dictionary


def thirty_top_words(unknown):
    """ Find 30 words with the highest ranks that do not belong to the dictionary. """
    return [term[0] for term in unknown[0:30]]  # they are sorted already


def three_occurrences(unknown):
    """ Find 30 words with 3 occurrences that do not belong to the dictionary. """
    return [term[0] for term in unknown if term[1] == 3][0:30]


def levenshtein(dictionary, frequency_list, invalid_words):
    """ Use Levenshtein distance and the frequency list, to determine the most probable correction of the words
    from the second list. """
    corrected_words = []
    for word in invalid_words:
        min_distance = 999
        min_distance_term = ""
        for (term, _) in frequency_list:
            if term not in dictionary:
                continue
            distance = Levenshtein.distance(word, term)
            if distance == 1:
                min_distance_term = term
                break
            elif distance < min_distance:
                min_distance = distance
                min_distance_term = term
        corrected_words.append(min_distance_term)
    return corrected_words


def print_results(top, three, corrected_words):
    print("30 words with the highest ranks that do not belong to the dictionary:")
    print(", ".join(top))
    print()
    print("30 words with 3 occurrences that do not belong to the dictionary:")
    print(", ".join(three))
    print()
    print("The most probable correction of the words from the previous list:")
    print(", ".join(corrected_words))


def main():
    all_frequency_lists = generate_frequency_lists()
    aggregated = aggregate_frequency_lists(all_frequency_lists)
    filtered = filter_frequency_list(aggregated)
    generate_plot(filtered)
    dictionary = load_dictionary()
    unknown = unknown_words(filtered, dictionary)
    top = thirty_top_words(unknown)
    three = three_occurrences(unknown)
    corrected_words = levenshtein(dictionary, filtered, three)
    print_results(top, three, corrected_words)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stop':
        remove_index()
    elif len(sys.argv) > 1 and sys.argv[1] == 'init':
        init()
    else:
        main()
