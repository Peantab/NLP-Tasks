import os
import regex


def ustawaCounter():
    counter = 0
    for file in generate_paths():
        with open(file, 'r') as inp:
            law = '\n'.join(inp.readlines())
            ustawa = regex.findall(r'(?:\bustawa\b)|(?:\bustawy\b)|(?:\bustaw\b)|(?:\bustawie\b)|(?:\bustawom\b)|(?:\bustawę\b)|(?:\bustawą\b)|(?:\bustawami\b)|(?:\bustawach\b)|(?:\bustawo\b)|(?:(?<=[\b\.])U\.)', law, regex.IGNORECASE)
            counter += len(ustawa)
    print(counter)


def generate_paths():
    (directory, _, filenames) = next(os.walk('ustawy'))
    return map(lambda name: os.path.join(directory, name), filenames)


if __name__ == '__main__':
    ustawaCounter()
