import requests
import re


def main():
    print(remove_unneeded(tag("Ala ma kota.")))


def tag(text):
    """ Use the tool to tag and lemmatize the corpus with the bills. """
    results = []
    r = requests.post('http://localhost:9200', data=text)
    word = ""
    assigned_tag = ""
    for line in r.text.splitlines():
        if not line.startswith("\t") and line is not "":
            word = line.split()[0].lower()
            assigned_tag = ""
        elif assigned_tag == "":
            assigned_tag = re.split("[\t:]", line)[2]
            results.append((word, assigned_tag))
    return results


def remove_unneeded(tagged_words):
    return [(word, assigned_tag) for (word, assigned_tag) in tagged_words if assigned_tag != "interp"]


if __name__ == '__main__':
    main()
