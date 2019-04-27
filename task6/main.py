import xml.etree.ElementTree as Et

nouns = dict()
synsets = dict()
synsets_backtrace = dict()
taxonomy_depth = dict()
synset_to_noun = dict()
hiperonymy_trace = []


def main():
    global synsets, taxonomy_depth, synsets_backtrace, synset_to_noun, nouns
    hiperonymy = '11'
    tree = Et.parse('plwordnet-4.0.xml')
    root = tree.getroot()
    for child in root:
        if child.tag == 'lexical-unit' and child.attrib['pos'] == 'rzeczownik':
            nouns[int(child.attrib['id'])] = child.attrib['name']
        elif child.tag == 'synset':
            is_noun = False
            for unit_id in child:
                if int(unit_id.text) in nouns:
                    synset_to_noun[int(child.attrib['id'])] = int(unit_id.text)
                    is_noun = True
                    break
            if is_noun:
                synsets[int(child.attrib['id'])] = []
        elif child.tag == 'synsetrelations' and child.attrib['relation'] == hiperonymy:
            relation_parent = int(child.attrib['parent'])
            relation_child = int(child.attrib['child'])
            if relation_parent in synsets and relation_child in synsets:
                synsets[relation_child].append(relation_parent)

    for key in synsets.keys():
        rec(key)

    result = max(taxonomy_depth.values())
    print(result)
    assemble_trace([x for (x, y) in taxonomy_depth.items() if y == result][0])
    print(" -> ".join(hiperonymy_trace))

    print("List of roots:")
    print(", ".join([nouns[synset_to_noun[word]] for word in [x for (x, y) in taxonomy_depth.items() if y == 1]]))


def rec(key):
    global synsets, taxonomy_depth, synsets_backtrace
    if key not in taxonomy_depth:
        candidates = [0]
        candidate_holders = [0]
        for hiponym in synsets[key]:
            candidates.append(rec(hiponym))
            candidate_holders.append(hiponym)
        taxonomy_depth[key] = max(candidates) + 1
        synsets_backtrace[key] = candidate_holders[candidates.index(taxonomy_depth[key] - 1)]
    return taxonomy_depth[key]


def assemble_trace(word):
    global hiperonymy_trace
    if word in synsets_backtrace and word != 0:
        hiperonymy_trace.append(nouns[synset_to_noun[word]])
        assemble_trace(synsets_backtrace[word])


if __name__ == '__main__':
    main()
