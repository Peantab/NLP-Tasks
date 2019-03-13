import os
import regex


DIRECTORY = 'ustawy'


def external_refs():
    collection = []
    waiting_for_dz_u = True
    file = 'ustawy/1994_195.txt'
    (this_year, this_pos) = year_and_position(file)
    content = file_content(file)
    year = this_year
    for token in regex.findall(r'(Dz\.U\.)|((?<=poz\.\s*)\d+)|(\d{4}(?=\s*r\.))|(załączniku)', content, regex.MULTILINE):
        (dz_u_token, pos_token, year_token, attachment_token) = token
        if dz_u_token != '':
            waiting_for_dz_u = False
        elif pos_token != '':
            pos = int(pos_token)
            if (year, pos) != (this_year, this_pos) and not waiting_for_dz_u:  # ignore the file signature and references in attachments; ignore references to attachments
                collection.append((year, pos))
        elif year_token != '':
            year = int(year_token)
        else:
            waiting_for_dz_u = True
    print(collection)


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
        return ''.join(inp.readlines())


def year_and_position(path):
    match = regex.search(DIRECTORY + os.path.sep + r'(?P<year>\d+)_(?P<pos>\d+)\.txt', path)
    return int(match['year']), int(match['pos'])


if __name__ == '__main__':
    external_refs()
