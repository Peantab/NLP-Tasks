import re
import xml.etree.ElementTree as Et
import matplotlib.pyplot as plt

FILE = 'output.xml'


def main():
    channels, occurrences = get_data_from_file(FILE)
    plot_fine(channels)
    plot_coarse(channels)
    fifty_most_frequent_named_entities(occurrences)
    ten_most_frequent_named_entities(occurrences)


def get_data_from_file(input_file):
    channels = dict()
    occurrences = dict()
    tree = Et.parse(input_file)
    root = tree.getroot()
    for chunk in root:
        for sentence in chunk:
            named_entities = dict()
            channels_in_sentence = dict()
            for token in sentence:
                if token.tag != 'tok':
                    continue
                text = ''
                for annotation in token:
                    if annotation.tag == 'lex':
                        for child in annotation:
                            if child.tag == 'base':
                                text = child.text
                    elif annotation.tag == 'ann':
                        channel = annotation.attrib['chan']
                        value = int(annotation.text)
                        if value != 0:
                            if (channel, value) not in named_entities:
                                named_entities[(channel, value)] = text
                            else:
                                named_entities[(channel, value)] += ' ' + text if text != '.' else '.'
                        if channel not in channels_in_sentence or channels_in_sentence[channel] < value:
                            channels_in_sentence[channel] = value
            for channel, value in channels_in_sentence.items():
                if channel not in channels:
                    channels[channel] = value
                else:
                    channels[channel] += value
            for ((channel, _), text) in named_entities.items():
                if (text, channel) not in occurrences:
                    occurrences[(text, channel)] = 1
                else:
                    occurrences[(text, channel)] += 1
    return channels, occurrences


def fifty_most_frequent_named_entities(named_entities: dict):
    as_list = list(named_entities.items())
    as_list.sort(key=lambda e: e[1], reverse=True)

    for ((text, channel), count) in as_list[:50]:
        print(text + ': ' + channel + '; count: ' + str(count))


def ten_most_frequent_named_entities(named_entities: dict):
    divided_by_coarse = dict()
    as_list = list(named_entities.items())
    as_list.sort(key=lambda e: e[1], reverse=True)

    for ((text, channel), count) in as_list:
        coarse_key = trim_coarse(channel)
        if coarse_key not in divided_by_coarse:
            divided_by_coarse[coarse_key] = [(text, count)]
        else:
            divided_by_coarse[coarse_key].append((text, count))

    for coarse_key, entries in divided_by_coarse.items():
        print(coarse_key + ':')
        for text, count in entries[:min(len(entries), 10)]:
            print('- ' + text + ': ' + str(count))


def plot_fine(fine):
    keys = []
    values = []
    sorted_channels = list(fine.items())
    sorted_channels.sort(key=lambda e: e[1], reverse=True)
    for key, value in sorted_channels:
        keys.append(key)
        values.append(value)
    plot(keys, values, 'Fine-grained classification histogram')


def plot_coarse(fine):
    coarse_channels = dict()
    for key, value in fine.items():
        coarse_key = trim_coarse(key)
        if coarse_key not in coarse_channels:
            coarse_channels[coarse_key] = value
        else:
            coarse_channels[coarse_key] += value
    keys = []
    values = []
    sorted_channels = list(coarse_channels.items())
    sorted_channels.sort(key=lambda e: e[1], reverse=True)
    for key, value in sorted_channels:
        keys.append(key)
        values.append(value)
    plot(keys, values, 'Coarse-grained classification histogram')


def trim_coarse(fine_label):
    return re.search(r'^(.*?_.*?)_.*', fine_label)[1]


def plot(keys, values, title):
    plt.rcdefaults()
    fig, ax = plt.subplots()

    ax.barh(keys, values, align='center', color='green')
    ax.set_yticks(range(len(keys)))
    ax.set_yticklabels(keys)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Occurrences')
    ax.set_title(title)
    for i, v in enumerate(values):
        ax.text(v + 3, i + .25, str(v), color='green')

    plt.show()


if __name__ == '__main__':
    main()
