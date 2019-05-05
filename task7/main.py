from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pickle
import random
import os

pos_mappings = {'noun': 'rzeczownik', 'adj': 'przymiotnik', 'verb': 'czasownik', 'num': 'liczebnik',
                'adv': 'przysłówek', 'pron': 'zaimek', 'prep': 'przyimek', 'conj': 'spójnik', 'interj': 'wykrzyknik',
                'burk': 'burk', 'qub': 'partykuła', 'xxx': 'xxx'}


def main():
    wv = load_word_vectors()

    most_similar(wv)
    equations(wv)
    t_sne(wv)


def load_word_vectors():
    file_name = "wv.pickle"
    if os.path.isfile(file_name):
        print("Loading word vectors from cache...", end="")
        with open(file_name, "rb") as f:
            wv = pickle.load(f)
    else:
        print("Loading word vectors from word2vec format...", end="")
        wv = KeyedVectors.load_word2vec_format('skipgram/skip_gram_v100m8.w2v.txt', binary=False)
        with open(file_name, "wb") as f:
            pickle.dump(wv, f)
    print("OK")
    return wv


def most_similar(wv):
    for word in ['sąd::noun', 'trybunał::noun', 'kodeks_cywilny::noun', 'kpk::noun', 'szkoda::noun', 'wypadek::noun',
                 'kolizja::noun', 'szkoda_majątkowa::noun', 'nieszczęście::noun', 'rozwód::noun']:
        # co z sąd wysoki, trybunał konstytucyjny, sąd rejonowy? - dałem zwykły sąd, trybunał
        result = wv.most_similar(positive=word, topn=20)
        print(crop_pos(word) + ":")
        for entry in result:
            (literal, pos) = extract_name_and_pos(entry[0])
            print('- {}: {}'.format(literal, pos))


def equations(wv):
    print('Wyniki obliczeń:')
    for vector in [wv.word_vec('sąd::noun') - wv.word_vec('kpc::noun') + wv.word_vec('konstytucja::noun'),
                   # sądu wysokiego nie ma
                   wv.word_vec('pasażer::noun') - wv.word_vec('mężczyzna::noun') + wv.word_vec('kobieta::noun'),
                   wv.word_vec('samochód::noun') - wv.word_vec('droga::noun') + wv.word_vec('rzeka::noun')]:
        result = wv.similar_by_vector(vector, topn=1)[0]
        (literal, pos) = extract_name_and_pos(result[0])
        print('- {}: {}'.format(literal, pos))


def t_sne(wv):
    # 'uszczerbek_na_zdrowiu' nie ma wśród wektorów, 'krzywda' również nie, ale jest 'krzywde'
    highlighted = ['szkoda::noun', 'strata::noun', 'uszczerbek::noun', 'szkoda_majątkowa::noun',
                   'krzywde::noun', 'niesprawiedliwość::noun', 'nieszczęście::noun']

    labels = []
    tokens = []
    highlighted_indices = []

    guaranteed_highlighted = random.sample(highlighted, 3)
    for highlightable in guaranteed_highlighted:
        tokens.append(wv.word_vec(highlightable))
        labels.append(crop_pos(highlightable))
        highlighted_indices.append(len(tokens) - 1)

    sample = random.sample(list(wv.vocab.keys()), 1000)
    for word in guaranteed_highlighted:
        if word in sample:
            sample.remove(word)
    sample = sample[:997]

    for word in sample:
        tokens.append(wv.word_vec(word))
        if word in highlighted:
            labels.append(crop_pos(word))
            highlighted_indices.append(len(tokens)-1)
        else:
            labels.append(crop_pos(word))

    tsne_model = TSNE(init='pca')
    embeddings = tsne_model.fit_transform(tokens)
    plot(embeddings, labels, highlighted_indices)


def plot(embeddings, labels, highlighted_indices):
    x = []
    y = []

    for value in embeddings:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        if i in highlighted_indices:
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         size=15,
                         color='red',
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
        else:
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
    plt.show()


def crop_pos(word):
    return word.split('::', maxsplit=1)[0]


def extract_name_and_pos(word):
    literal, pos = word.split('::', maxsplit=1)
    pos = pos_mappings[pos]
    return literal, pos


if __name__ == '__main__':
    main()
