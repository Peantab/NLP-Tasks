import os
import errno
import re

DIRECTORY = '../ustawy'

INITIAL_BILLS_DIR = './initial/'
AMENDING_BILLS_DIR = './amending/'


def main():
    confirm_dirs()
    for name, file in generate_names_and_paths():
        bill = file_content(file)

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
    print('OK')


def generate_names_and_paths():
    (_, _, filenames) = next(os.walk(DIRECTORY))
    return zip(filenames, map(lambda name: os.path.join(DIRECTORY, name), filenames))


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


if __name__ == '__main__':
    main()
