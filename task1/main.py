import os
import sys
import regex


DIRECTORY = 'ustawy'


def external_refs():
    """ Task 1 """
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


def internal_refs():
    """ Task 2 """
    collection = []
    for file in generate_paths():
        collection_in_file = []
        (year, pos) = year_and_position(file)
        content = file_content(file)
        content = ignore_quotations_and_names(content)
        content = skip_changelogs(content)
        article = 0
        for token in regex.findall(r'((?<=art\.\s*)\d+(?!\.))|((?<=ust\.\s*)\d+\b(?!(?:\s+ustawy\s+zmienianej)|(?:\s+pkt\s+\d\s+ustawy\s+zmienianej)))', content, regex.MULTILINE + regex.IGNORECASE):
            (art_token, paragraph_token) = token
            if art_token != '':
                article = int(art_token)
            else:
                paragraph = int(paragraph_token)
                collection_in_file.append((article, paragraph))

        collection_in_file.sort(key=lambda p: p[1])
        collection_in_file.sort(key=lambda p: p[0])
        aggregated = count_duplicates(collection_in_file)
        aggregated.sort(key=lambda p: p[2], reverse=True)

        for record in aggregated:
            collection.append((year, pos, record[0], record[1], record[2]))

    collection.sort(key=lambda p: p[1])
    collection.sort(key=lambda p: p[0])
    csv_task_two(collection)


def ustawa_counter():
    """ Task 3 """
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
    if len(collection) == 0:
        return output
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
    output.append((last_year, last_pos, last_issue, counter))
    return output


def csv_task_one(collection):
    print('"Rok","Pozycja","Nr","Liczba referencji"')
    for record in collection:
        print("{},{},{},{}".format(record[0], record[1], record[2], record[3]))


def ignore_quotations_and_names(text):
    """ If it's a quotation, it surely doesn't have references to quoting document """
    return regex.sub(r"[\"„].*?[\"”]", "", text, flags=regex.MULTILINE+regex.DOTALL)


def skip_changelogs(text):
    """ Skip articles announcing changes introduced in other bill """
    split = regex.split(r"(?=\bArt\.).", text)
    split = list(filter(lambda article: regex.search(r"wprowadza\s+się\s+następujące\s+zmiany:", article, flags=regex.MULTILINE) is None, split))
    result = "A".join(split)
    return result


def count_duplicates(collection):
    output = []
    counter = 0
    if len(collection) == 0:
        return output
    last_entry = collection[0]
    for entry in collection:
        if entry != last_entry:
            output.append((last_entry[0], last_entry[1], counter))
            counter = 0
        last_entry = entry
        counter += 1
    output.append((last_entry[0], last_entry[1], counter))
    return output


def csv_task_two(collection):
    print('"Rok","Pozycja","Artykuł","Ustęp","Liczba referencji"')
    for record in collection:
        print("{},{},{},{},{}".format(record[0], record[1], record[2], record[3], record[4]))


if __name__ == '__main__':
    if (len(sys.argv) >= 2):
        arg = int(sys.argv[1])
        if arg == 1:
            external_refs()
        elif arg == 2:
            internal_refs()
        elif arg == 3:
            ustawa_counter()
    else:
        internal_refs()
