import os
import re

DIRECTORY = '../ustawy'


def main():
    corpora = load_corpora()
    bigrams = count_bigrams(corpora)


def load_corpora():
    """ The text has to be properly normalized before the counts are computed: it should be downcased
    and all punctuation should be removed. """
    corpora = []
    for file in generate_paths():
        bill = file_content(file)
        bill = re.sub(r'\W+', ' ', bill)
        bill = bill.lower()
        corpora.append(bill)
    return corpora


def count_bigrams(corpora):
    """ Compute bigram counts in the corpora, ignoring bigrams which contain at least one token that is not a word
    (it contains characters other than letters). """
    bigrams = dict()
    for bill in corpora:
        words = bill.split()
        for (first, second) in zip(words[0:len(words)-1], words[1:len(words)]):
            if not re.search(r'[0-9_]', first+second):
                if (first, second) not in bigrams:
                    bigrams[(first, second)] = 1
                else:
                    bigrams[(first, second)] += 1
    return bigrams


def generate_paths():
    (_, _, filenames) = next(os.walk(DIRECTORY))
    return map(lambda name: os.path.join(DIRECTORY, name), filenames)


def file_content(path):
    with open(path, 'r') as inp:
        return ''.join(inp.readlines())


if __name__ == '__main__':
    main()
