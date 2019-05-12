import os
import re
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

DATA_DIRECTORY = './data'

FULL_TEXT = 'full_text'
TEN_PERCENT = 'ten_percent'
TEN_LINES = 'ten_lines'
ONE_LINE = 'one_line'

TARGET = FULL_TEXT


def main():
    test_file = TARGET + '_tes.csv'
    # dev_file = TARGET + '_val.csv'
    train_file = TARGET + '_tra.csv'

    stop_words = prepare_stopwords()
    train_x, y_train = read_input_file(train_file)
    test_x, y_test = read_input_file(test_file)
    genres = list(set(y_train))

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words=stop_words)),
        ('clf', OneVsRestClassifier(LinearSVC(), n_jobs=1)),
    ])
    parameters = {
        'tfidf__max_df': (0.25, 0.5, 0.75),
        'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
        "clf__estimator__C": [0.01, 0.1, 1],
        "clf__estimator__class_weight": ['balanced', None],
    }
    grid_search(train_x, y_train, test_x, y_test, genres, parameters, pipeline)


def prepare_stopwords():
    with open('stopwords-pl.txt', 'r') as stopwords_file:
        stopwords = [stopword[:-1] for stopword in stopwords_file.readlines()]
    return stopwords


def read_input_file(input_file):
    tags = []
    bills = []
    with open(os.path.join(DATA_DIRECTORY, input_file), 'r') as opened_file:
        for line in opened_file.readlines():
            parsed = re.fullmatch(r'(\w+)\t(.*)\n', line)
            tags.append(parsed.group(1))
            bills.append(parsed.group(2))
    return bills, tags


def grid_search(train_x, train_y, test_x, test_y, genres, parameters, pipeline):
    grid_search_tune = GridSearchCV(pipeline, parameters, cv=2, n_jobs=3, verbose=10)
    grid_search_tune.fit(train_x, train_y)

    print("Best parameters set:")
    print(grid_search_tune.best_estimator_.steps)

    # measuring performance on test set
    print("Applying best classifier on test data:")
    best_clf = grid_search_tune.best_estimator_
    predictions = best_clf.predict(test_x)

    print(classification_report(test_y, predictions, target_names=genres))


if __name__ == '__main__':
    main()
