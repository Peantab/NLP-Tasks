import os
import errno
import re
import random

DIRECTORY = '../ustawy'

INITIAL_BILLS_DIR = './initial/'
AMENDING_BILLS_DIR = './amending/'


def main():
    confirm_dirs()
    for name, path in generate_names_and_paths(DIRECTORY):
        bill = file_content(os.path.join(path, name))

        # Recognize a type
        found_patterns = re.search(r'^\W*(?:zmieniająca\W+ustawę\W+)?o\W+zmianie(?:\W+niektórych)?\W+ustaw',
                                   bill, re.IGNORECASE + re.MULTILINE)
        new_localisation = INITIAL_BILLS_DIR if found_patterns is None else AMENDING_BILLS_DIR
        new_localisation += name

        # Strip header
        bill = re.sub(r'.*?^((?=\W*Art\.\W*1)|(?=\W*Rozdział))', '', bill, 1, re.IGNORECASE + re.MULTILINE + re.DOTALL)

        # Remove empty lines
        bill = re.sub(r'^\W*\n', '', bill, 0, re.MULTILINE)

        # Save to a file
        with open(new_localisation, "w+") as new_copy:
            new_copy.write(bill)
    split_into_groups()
    print('OK')


def generate_names_and_paths(directory):
    (_, _, filenames) = next(os.walk(directory))
    return [(name, directory) for name in filenames]


def file_content(path):
    with open(path, 'r') as inp:
        return ''.join(inp.readlines())


def confirm_dirs():
    for directory in [INITIAL_BILLS_DIR, AMENDING_BILLS_DIR]:
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def split_into_groups():
    for directory in [INITIAL_BILLS_DIR, AMENDING_BILLS_DIR]:
        files = generate_names_and_paths(directory)
        files_count = len(files)
        sixty_percent = int(0.6 * files_count)
        twenty_percent = int(0.2 * files_count)
        random.shuffle(files)
        training = files[:sixty_percent]
        validation = files[sixty_percent:sixty_percent + twenty_percent]
        testing = files[sixty_percent + twenty_percent:]
        for pack, prefix in [(training, 'tra_'), (validation, 'val_'), (testing, 'tes_')]:
            for name, path in pack:
                os.rename(os.path.join(path, name), os.path.join(path, prefix + name))


if __name__ == '__main__':
    main()
