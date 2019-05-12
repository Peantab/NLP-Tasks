import os
from fastText import train_supervised

DATA_DIRECTORY = './data'

FULL_TEXT = 'full_text'
TEN_PERCENT = 'ten_percent'
TEN_LINES = 'ten_lines'
ONE_LINE = 'one_line'

TARGET = FULL_TEXT


def main():
    # test_file = TARGET + '_tes.csv'
    # valid_file = TARGET + '_val.csv'
    train_file = TARGET + '_tra.csv'

    train_data = os.path.join(DATA_DIRECTORY, train_file)

    # train_supervised uses the same arguments and defaults as the fastText cli
    model = train_supervised(input=train_data, epoch=10, lr=1.0, wordNgrams=2, verbose=2, minCount=1)

    model.save_model('fasttext_' + TARGET + ".bin")


if __name__ == '__main__':
    main()
