from gensim.models import KeyedVectors

pos_mappings = {'noun': 'rzeczownik', 'adj': 'przymiotnik', 'verb': 'czasownik', 'num': 'liczebnik',
                'adv': 'przysłówek', 'pron': 'zaimek', 'prep': 'przyimek', 'conj': 'spójnik', 'interj': 'wykrzyknik',
                'burk': 'burk', 'qub': 'partykuła', 'xxx': 'xxx'}


def main():
    wv = KeyedVectors.load_word2vec_format('skipgram/skip_gram_v100m8.w2v.txt', binary=False)
    for word in ['sąd::noun', 'trybunał::noun', 'kodeks_cywilny::noun', 'kpk::noun', 'szkoda::noun', 'wypadek::noun',
                 'kolizja::noun', 'szkoda_majątkowa::noun', 'nieszczęście::noun', 'rozwód::noun']:
        # co z sąd wysoki, trybunał konstytucyjny, sąd rejonowy? - dałem zwykły sąd, trybunał
        result = wv.most_similar(positive=word, topn=20)
        print(word.split('::', maxsplit=1)[0] + ":")
        for entry in result:
            (literal, pos) = entry[0].split('::', maxsplit=1)
            pos = pos_mappings[pos]
            print('- {}: {}'.format(literal, pos))

    print('Wyniki obliczeń:')
    for vector in [wv.word_vec('sąd::noun') - wv.word_vec('kpc::noun') + wv.word_vec('konstytucja::noun'),  # sądu wysokiego nie ma
                   wv.word_vec('pasażer::noun') - wv.word_vec('mężczyzna::noun') + wv.word_vec('kobieta::noun'),
                   wv.word_vec('samochód::noun') - wv.word_vec('droga::noun') + wv.word_vec('rzeka::noun')]:
        result = wv.similar_by_vector(vector, topn=1)[0]
        (literal, pos) = result[0].split('::', maxsplit=1)
        pos = pos_mappings[pos]
        print('- {}: {}'.format(literal, pos))
    pass


if __name__ == '__main__':
    main()
