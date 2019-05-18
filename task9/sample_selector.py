import os
import errno
import random

INPUT_DIRECTORY = '../ustawy'
SELECTED_BILLS_DIRECTORY = './selected'


def main():
    confirm_dir(SELECTED_BILLS_DIRECTORY)
    files = generate_names_and_paths(INPUT_DIRECTORY)
    random_100 = random.sample(files, 100)
    batch = []
    batch_no = 0

    for name, path in random_100:
        bill = file_content(os.path.join(path, name))
        batch.append(bill)
        # Save to a file
        with open(os.path.join(SELECTED_BILLS_DIRECTORY, name), 'w+', encoding="utf8") as new_copy:
            new_copy.write(bill)
        if len(batch) == 10:
            with open(os.path.join(SELECTED_BILLS_DIRECTORY, "batch_" + str(batch_no)), 'w+', encoding="utf8") as new_copy:
                new_copy.write('\n'.join(batch))
            batch = []
            batch_no += 1


def confirm_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def generate_names_and_paths(directory):
    (_, _, filenames) = next(os.walk(directory))
    return [(name, directory) for name in filenames]


def file_content(path):
    with open(path, 'r', encoding="utf8") as inp:
        return ''.join(inp.readlines())


if __name__ == '__main__':
    main()
