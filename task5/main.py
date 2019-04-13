import requests
import pickle
import math
import os
import re

DIRECTORY = '../ustawy'


def main():
    corpora = load_corpora()
    bigrams = count_bigrams(corpora)
    probability_calculator = ProbabilityCalculator(bigrams)
    llr_results = log_likelihood_ratio(bigrams, probability_calculator)
    top_fifty = top_fifty_noun_based(llr_results)
    print_results(top_fifty)


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


def count_bigrams(corpora):
    """ Using the tagged corpus compute bigram statistic for the tokens containing:
        * lemmatized, downcased word
        * morphosyntactic category of the word (noun, verb, etc.)"""
    bigrams = dict()
    for bill in corpora:
        for (first, second) in zip(bill[0:len(bill)-1], bill[1:len(bill)]):
            if not re.search(r'[0-9_]', first[0]+second[0]) and not first[0] == "" and not second[0] == "":
                if (first, second) not in bigrams:
                    bigrams[(first, second)] = 1
                else:
                    bigrams[(first, second)] += 1
    return bigrams


def log_likelihood_ratio(bigrams, probability_calculator):
    """ Compute LLR statistic for this dataset. """
    print("Counting LLR...", end="")
    bigrams_with_llr = []
    for (x, y) in bigrams.keys():
        value = llr_2x2(probability_calculator.both(x, y),
                        probability_calculator.right_no_left(x, y),
                        probability_calculator.left_no_right(x, y),
                        probability_calculator.no_left_no_right(x, y))
        bigrams_with_llr.append(((x, y), value))
    print("OK")
    return sorted(bigrams_with_llr, key=(lambda e: e[1]), reverse=True)


def top_fifty_noun_based(llr_results):
    """ Select top 50 results including noun at the first position and noun or adjective at the second position. """
    noun = "subst"
    adjective_or_noun = {"adj", "adja", "adjp", "adjc", noun}
    return [(left, right) for ((left, right), _) in llr_results
            if left[1] == noun and right[1] in adjective_or_noun][:50]


def print_results(results):
    print()
    print("Top 50 results including noun at the first position and noun or adjective at the second position:")
    print(", ".join([left[0] + " " + right[0] for (left, right) in results]))
    with open("results.txt", "w") as results_file:
        results_file.write("\n".join([left[0] + " " + right[0] for (left, right) in results]))


def generate_paths():
    (_, _, filenames) = next(os.walk(DIRECTORY))
    return map(lambda name: os.path.join(DIRECTORY, name), filenames)


def file_content(path):
    with open(path, 'r') as inp:
        return ''.join(inp.readlines())


class ProbabilityCalculator:
    def __init__(self, bigrams):
        print("Caching probability data...", end="")
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
        print("OK")

    def left(self, word):
        nominator = self.occurrences[word][0]
        return nominator/self.denominator

    def right(self, word):
        nominator = self.occurrences[word][1]
        return nominator/self.denominator

    def left_no_right(self, word_left, word_right):
        nominator = self.occurrences[word_left][0] - self.bigrams[(word_left, word_right)]
        return nominator/self.denominator

    def right_no_left(self, word_left, word_right):
        nominator = self.occurrences[word_right][1] - self.bigrams[(word_left, word_right)]
        return nominator/self.denominator

    def no_left_no_right(self, word_left, word_right):
        nominator = self.denominator - self.occurrences[word_left][0] - self.occurrences[word_right][1]
        if (word_left, word_right) in self.bigrams.keys():
            nominator += self.bigrams[(word_left, word_right)]
        return nominator / self.denominator

    def any(self, word):
        # not used but kept here for making possible not distinguishing between "left" and "right" word.
        nominator = self.occurrences[word][0] + self.occurrences[word][1]
        if (word, word) in self.bigrams.keys():
            nominator -= self.bigrams[(word, word)]
        return nominator/self.denominator

    def both(self, word_left, word_right):
        nominator = self.bigrams[(word_left, word_right)]
        return nominator/self.denominator


# The two functions below come from python-llr library by Ted Dunning (https://github.com/tdunning/python-llr)
def llr_2x2(k11, k12, k21, k22):
    """ Special case of llr with a 2x2 table """
    return 2 * (denormEntropy([k11+k12, k21+k22]) +
                denormEntropy([k11+k21, k12+k22]) -
                denormEntropy([k11, k12, k21, k22]))


def denormEntropy(counts):
    """ Computes the entropy of a list of counts scaled by the sum of the counts.
    If the inputs sum to one, this is just the normal definition of entropy """
    counts = list(counts)
    total = float(sum(counts))
    # Note tricky way to avoid 0*log(0)
    return -sum([k * math.log(k/total + (k == 0)) for k in counts])


if __name__ == '__main__':
    main()
