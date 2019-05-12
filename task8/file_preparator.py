import os
import errno
import re
import random

DIRECTORY = '../ustawy'

DATA_DIRECTORY = './data'

INITIAL_BILLS_DIR = './initial'
AMENDING_BILLS_DIR = './amending'

TEN_PERCENT = 'ten_percent'
TEN_LINES = 'ten_lines'
ONE_LINE = 'one_line'


def main():
    copy_and_recognize()
    split_into_groups()
    generate_shortened_versions()
    fasttextise()
    prepare_input()
    print('OK')


def copy_and_recognize():
    confirm_dirs()
    for name, path in generate_names_and_paths(DIRECTORY):
        bill = file_content(os.path.join(path, name))

        # Recognize a type
        found_patterns = re.search(r'^\W*(?:zmieniająca\W+ustawę\W+)?o\W+zmianie(?:\W+niektórych)?\W+ustaw',
                                   bill, re.IGNORECASE + re.MULTILINE)
        new_localisation = INITIAL_BILLS_DIR if found_patterns is None else AMENDING_BILLS_DIR
        new_localisation = os.path.join(new_localisation, name)

        # Strip header
        bill = re.sub(r'.*?^((?=\W*Art\.\W*1)|(?=\W*Rozdział))', '', bill, 1, re.IGNORECASE + re.MULTILINE + re.DOTALL)

        # Remove empty lines
        bill = re.sub(r'^\W*\n', '', bill, 0, re.MULTILINE)

        # Remove final newline
        bill = re.sub(r'\n\Z', '', bill, 0, re.MULTILINE)

        # Save to a file
        with open(new_localisation, 'w+', encoding="utf8") as new_copy:
            new_copy.write(bill)


def generate_names_and_paths(directory):
    (_, _, filenames) = next(os.walk(directory))
    return [(name, directory) for name in filenames]


def file_content(path):
    with open(path, 'r', encoding="utf8") as inp:
        return ''.join(inp.readlines())


def confirm_dirs(suffix=''):
    for directory in [INITIAL_BILLS_DIR, AMENDING_BILLS_DIR]:
        confirm_dir(directory + suffix)


def confirm_dir(directory):
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


def generate_shortened_versions():
    for suffix, amount in [('_' + TEN_PERCENT, lambda x: max(int(0.1 * x), 1)),
                           ('_' + TEN_LINES, lambda x: min(10, x)),
                           ('_' + ONE_LINE, lambda x: min(1, x))]:
        confirm_dirs(suffix)
        for directory in [INITIAL_BILLS_DIR, AMENDING_BILLS_DIR]:
            for name, path in generate_names_and_paths(directory):
                bill = file_content(os.path.join(path, name))
                lines = bill.split('\n')
                amount_to_take = amount(len(lines))
                to_save = random.sample(lines, amount_to_take)
                with open(os.path.join(directory + suffix, name), 'w+', encoding="utf8") as output:
                    output.write('\n'.join(to_save))


def fasttextise():
    """ Generate files in FastText format """
    for classification, class_dir in [('initial', INITIAL_BILLS_DIR), ('amending', AMENDING_BILLS_DIR)]:
        label = '__label__' + classification
        for subdir in ['', '_' + TEN_PERCENT, '_' + TEN_LINES, '_' + ONE_LINE]:
            path = class_dir + subdir
            entries_tra = []
            entries_tes = []
            entries_val = []
            for name, path_2 in generate_names_and_paths(path):
                bill = file_content(os.path.join(path_2, name))
                bill = re.sub(r'\n', ' ', bill)  # substitute line breaks with spaces
                bill = re.sub(r'  +', ' ', bill)  # at most one space in row
                if name.startswith('tes'):
                    entries_tes.append(label + '\t' + bill)
                elif name.startswith('tra'):
                    entries_tra.append(label + '\t' + bill)
                elif name.startswith('val'):
                    entries_val.append(label + '\t' + bill)
            with open(os.path.join(path, 'fasttext_tra.csv'), 'w+', encoding="utf8") as fasttext:
                fasttext.write('\n'.join(entries_tra))
            with open(os.path.join(path, 'fasttext_tes.csv'), 'w+', encoding="utf8") as fasttext:
                fasttext.write('\n'.join(entries_tes))
            with open(os.path.join(path, 'fasttext_val.csv'), 'w+', encoding="utf8") as fasttext:
                fasttext.write('\n'.join(entries_val))


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


if __name__ == '__main__':
    main()
