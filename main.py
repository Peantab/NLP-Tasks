import os
import regex


DIRECTORY = 'ustawy'


def external_refs():
    file = 'ustawy/1993_599.txt'
    (year, pos) = year_and_position(file)
    example = file_content(file)
    print(year, ' ', pos)


def ustawa_counter():
    counter = 0
    for file in generate_paths():
        law = file_content(file)
        ustawa = regex.findall(r'(?:\bustawa\b)|(?:\bustawy\b)|(?:\bustaw\b)|(?:\bustawie\b)|(?:\bustawom\b)|(?:\bustawę\b)|(?:\bustawą\b)|(?:\bustawami\b)|(?:\bustawach\b)|(?:\bustawo\b)|(?:(?<=[\b\.])U\.)', law, regex.IGNORECASE)
        counter += len(ustawa)
    print(counter)


def generate_paths():
    (_, _, filenames) = next(os.walk(DIRECTORY))
    return map(lambda name: os.path.join(DIRECTORY, name), filenames)


def file_content(path):
    with open(path, 'r') as inp:
        return '\n'.join(inp.readlines())


def year_and_position(path):
    match = regex.search(DIRECTORY + os.path.sep + r'(?P<year>\d+)_(?P<pos>\d+)\.txt', path)
    return match['year'], match['pos']


if __name__ == '__main__':
    external_refs()
