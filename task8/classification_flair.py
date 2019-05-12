import os
import errno
from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path

DATA_DIRECTORY = './data'

TEN_PERCENT = 'ten_percent'
TEN_LINES = 'ten_lines'
ONE_LINE = 'one_line'

TARGET = TEN_PERCENT


def main():
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


if __name__ == '__main__':
    main()
