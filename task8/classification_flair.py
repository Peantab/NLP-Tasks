import os
import random
import errno
from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path

DATA_DIRECTORY = './data'

INITIAL_BILLS_DIR = './initial'
AMENDING_BILLS_DIR = './amending'

TEN_PERCENT = 'ten_percent'
TEN_LINES = 'ten_lines'
ONE_LINE = 'one_line'

TARGET = TEN_PERCENT


def main():
    # prepare_input()

    test_file = TARGET + '_tes.csv'
    dev_file = TARGET + '_val.csv'
    train_file = TARGET + '_tra.csv'

    corpus = NLPTaskDataFetcher.load_classification_corpus(Path(DATA_DIRECTORY), test_file=test_file, dev_file=dev_file,
                                                           train_file=train_file)
    word_embeddings = [WordEmbeddings('pl'), FlairEmbeddings('polish-forward'),
                       FlairEmbeddings('polish-backward')]
    document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=512, reproject_words=True,
                                                 reproject_words_dimension=256)
    classifier = TextClassifier(document_embeddings, label_dictionary=corpus.make_label_dictionary(), multi_label=False)
    trainer = ModelTrainer(classifier, corpus)
    trainer.train('./', max_epochs=10)


def prepare_input():
    confirm_dir(DATA_DIRECTORY)
    for variant, directory_suffix in [('full_text', ''), ('ten_percent', '_' + TEN_PERCENT),
                                      ('ten_lines', '_' + TEN_LINES), ('one_line', '_' + ONE_LINE)]:
        for part in ['_tra', '_val', '_tes']:
            fasttext_list = []
            for class_dir in [INITIAL_BILLS_DIR, AMENDING_BILLS_DIR]:
                with open(os.path.join(class_dir + directory_suffix, 'fasttext' + part + '.csv'), encoding="utf8")\
                        as fasttext_file:
                    fasttext_list.extend(fasttext_file.readlines())
            random.shuffle(fasttext_list)
            with open(os.path.join(DATA_DIRECTORY, variant + part + '.csv'), 'w', encoding="utf8") as output:
                output.write(''.join(fasttext_list))


def confirm_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    main()
