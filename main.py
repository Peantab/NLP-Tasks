import os
import regex


DIRECTORY = 'ustawy'


def external_refs():
    collection = []
    waiting_for_dz_u = True
    for file in generate_paths():
        (this_year, this_pos) = year_and_position(file)
        content = file_content(file)
        year = this_year
        issue_no = 0
        for token in regex.findall(r'(Dz\.\s*U\.)|((?<=poz\.\s*)\d+)|(\d{4}(?=\s*r\.))|(załączniku)|((?<=Nr\s*)\d+)',
                                   content, regex.MULTILINE):
            (dz_u_token, pos_token, year_token, attachment_token, number_token) = token
            if dz_u_token != '':
                waiting_for_dz_u = False
            elif pos_token != '':
                pos = int(pos_token)
                # ignore the file signature and references in attachments; ignore references to attachments
                if (year, pos) != (this_year, this_pos) and not waiting_for_dz_u:
                    collection.append((year, pos, issue_no))
                    issue_no = 0
            elif year_token != '':
                year = int(year_token)
            elif attachment_token != '':
                waiting_for_dz_u = True
            else:
                issue_no = int(number_token)

    collection.sort(key=lambda p: p[1])
    collection.sort(key=lambda p: p[0])
    aggregated = pseudo_functional_stuff(collection)
    aggregated.sort(key=lambda p: p[3], reverse=True)

    csv_task_one(aggregated)


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


def pseudo_functional_stuff(collection):
    """ It's groupBy, reduce and map, apparently the Python-way... :( """
    output = []
    last_year = collection[0][0]
    last_pos = collection[0][1]
    last_issue = 0
    counter = 0
    for (year, pos, issue_no) in collection:
        if year != last_year or pos != last_pos:
            output.append((last_year, last_pos, last_issue, counter))
            counter = 0
        last_year = year
        last_pos = pos
        last_issue = issue_no
        counter += 1
    return output


def csv_task_one(collection):
    print('"Rok","Pozycja","Nr","Liczba referencji"')
    for record in collection:
        print("{},{},{},{}".format(record[0], record[1], record[2], record[3]))


if __name__ == '__main__':
    external_refs()
