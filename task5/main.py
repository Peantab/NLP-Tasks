import requests
import pickle
import os
import re

DIRECTORY = '../ustawy'


def main():
    corpora = load_corpora()


def load_corpora():
    file_name = "corpora.pickle"
    corpora = []
    if os.path.isfile(file_name):
        print("Loading corpora from file (running Docker is not needed)...", end="")
        with open(file_name, "rb") as f:
            corpora = pickle.load(f)
    else:
        print("Generating corpora...", end="")
        for file in generate_paths():
            bill = file_content(file)
            tagged_bill = remove_unneeded(tag(bill))
            corpora.append(tagged_bill)
        with open(file_name, "wb") as f:
            pickle.dump(corpora, f)
    print("OK")
    return corpora


def tag(text):
    """ Use the tool to tag and lemmatize the corpus with the bills. """
    results = []
    r = requests.post('http://localhost:9200', data=text.encode('utf-8'))
    seek = False
    for line in r.text.splitlines():
        if not line.startswith("\t") and line is not "":
            seek = True
        elif seek is True and line is not "":
            line_tokens = re.split("[\t:]", line)
            results.append((line_tokens[1].lower(), line_tokens[2]))
    return results


def remove_unneeded(tagged_words):
    return [(word, assigned_tag) for (word, assigned_tag) in tagged_words if assigned_tag != "interp"]


def generate_paths():
    (_, _, filenames) = next(os.walk(DIRECTORY))
    return map(lambda name: os.path.join(DIRECTORY, name), filenames)


def file_content(path):
    with open(path, 'r') as inp:
        return ''.join(inp.readlines())


if __name__ == '__main__':
    main()
