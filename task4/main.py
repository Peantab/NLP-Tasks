import os
import re
import math

DIRECTORY = '../ustawy'


def main():
    corpora = load_corpora()
    bigrams = count_bigrams(corpora)
    probability_calculator = ProbabilityCalculator(bigrams)
    pmi_results = pointwise_mutual_information(bigrams, probability_calculator)
    display_top_thirty("Top 30 results for Pointwise Mutual Information:", pmi_results)


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


def pointwise_mutual_information(bigrams, probability_calculator):
    """ Use pointwise mutual information to compute the measure for all pairs of words. """
    bigrams_with_pmi = []
    for (x, y) in bigrams:
        no_log = probability_calculator.both(x, y) / (probability_calculator.left(x) * probability_calculator.right(y))
        bigrams_with_pmi.append(((x, y), math.log2(no_log)))
    return sorted(bigrams_with_pmi, key=(lambda e: e[1]), reverse=True)


def display_top_thirty(description, data):
    print(description)
    top_30 = ", ".join([left+" "+right for ((left, right), _) in data[:30]])
    print(top_30)


class ProbabilityCalculator:
    def __init__(self, bigrams):
        self.bigrams = bigrams
        all_words = set()
        all_words.update([left for (left, _) in self.bigrams.keys()])
        all_words.update([right for (_, right) in self.bigrams.keys()])
        self.occurrences = {word: (0, 0) for word in all_words}
        self.denominator = 0
        for ((left, right), count) in self.bigrams.items():
            self.occurrences[left] = (self.occurrences[left][0] + count, self.occurrences[left][1])
            self.occurrences[right] = (self.occurrences[right][0], self.occurrences[right][1] + count)
            self.denominator += count

    def left(self, word):
        nominator = self.occurrences[word][0]
        return nominator/self.denominator

    def right(self, word):
        nominator = self.occurrences[word][1]
        return nominator/self.denominator

    def any(self, word):
        nominator = self.occurrences[word][0] + self.occurrences[word][1]
        if (word, word) in self.bigrams.keys():
            nominator -= self.bigrams[(word, word)]
        return nominator/self.denominator

    def both(self, word_left, word_right):
        nominator = self.bigrams[(word_left, word_right)]
        return nominator/self.denominator


def generate_paths():
    (_, _, filenames) = next(os.walk(DIRECTORY))
    return map(lambda name: os.path.join(DIRECTORY, name), filenames)


def file_content(path):
    with open(path, 'r') as inp:
        return ''.join(inp.readlines())


if __name__ == '__main__':
    main()
