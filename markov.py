from random import choice as choose
from random import random as r
from random import randint


def chance(c):
    """
    Returns True with the given probability, and False otherwise.
    :param c: The chance to return True.
    :return: True or False randomly.  Always True if c >= 1.0, and always False if c <= 0.0.
    """
    return c > r()


def terminates_sentence(word, terminators=("!", "?", "."), non_terminators=("...",)):
    """
    Determines whether or not the given word terminates the sentence.
    :param word: The word to test.
    :param terminators: A sequence of strings that terminate a sentence.
    :param non_terminators: A sequence of strings that do not terminate a sentence.
    :return: True if the word terminates the sentence.
    """
    for non_terminator in non_terminators:
        if word.endswith(non_terminator):
            return False

    for terminator in terminators:
        if word.endswith(terminator):
            return True


def add_dict_entry(dictionary, key, value):
    """
    Either initializes the given key in the given dictionary with a list containing the given value, or adds to the list
    if it already exists.
    :param dictionary: The dictionary to update.
    :param key: The key to update.
    :param value: The value to append.
    :return: None.  The dictionary is modified in-place.
    """
    try:
        dictionary[key].append(value)
    except KeyError:
        dictionary[key] = [value]


def superstrip(word, stripables=(".", "...", "?", "!", "(", ")", ",")):
    """
    Strips a word of all given strings.
    :param word: The word to strip.
    :param stripables: The sequence of strings to strip from the word.
    :return: The word stripped of all stripables.
    """
    if word is None:
        return None
    simple = word
    for stripable in stripables:
        simple = simple.replace(stripable, "")
    return simple.lower()


def read_paragraphs(fp, delete):
    """
    Reads a text file as a sequence of paragraphs.  Paragraphs are considered all text between two pairs of newlines.
    :param fp: The path to the text file.
    :param delete: A sequence of strings that should be deleted from the text.
    :return: A list of paragraphs from the text.
    """
    paragraphs = []

    with open(fp) as f:
        thisParagraph = ""
        for line in f:
            for term in delete:
                line = line.replace(term, "")

            if len(line.strip()) == 0:
                paragraphs.append(thisParagraph[:-1])
                thisParagraph = ""
            else:
                thisParagraph += line + " "
        if len(thisParagraph.strip()) > 0:
            paragraphs.append(thisParagraph[:-1])
        f.close()

    return paragraphs


def random_slice(l, size):
    """
    Picks a random slice out of the list with a given size.
    :param l: The list from which to take a slice.
    :param size: The size of the slice.
    :return: A slice of the list.
    """
    first = randint(0, len(l) - size)
    return l[first:first+size]


def create_superdict(paragraphs):
    """
    Creates the superdictionary from the given paragraphs.
    :param paragraphs: The paragraphs.
    :return: The superdictionary.
    """
    d = dict()

    for para in paragraphs:
        words = para.split(" ")
        words = [word for word in words if len(word) > 0]

        # First word succeeds null.
        add_dict_entry(d, None, words[0])

        for w in range(len(words) - 1):
            a, b = words[w:w + 2]
            if terminates_sentence(a):
                add_dict_entry(d, a, None)
                add_dict_entry(d, None, b)
            else:
                add_dict_entry(d, a, b)

            # addAliasEntry(alias, a)

        # Last word preceeds null.
        add_dict_entry(d, words[-1], None)

    return d


def generate_text(d, maximum_text_length=280, chance_to_exit_when_sentence_terminates=0.375,
                  sentence_separator=" ", overflow_indicator="..."):
    """
    Generates text using the given superdictionary.
    :param d: The superdictionary.
    :param maximum_text_length: The maximum length the text may have.  Default 280.
    :param chance_to_exit_when_sentence_terminates: The chance that the procedure exits after each sentence terminates.
    Default 0.375 (37.5% chance).
    :param sentence_separator: The text that is inserted when a sentence terminates.  Default ' ' (one whitespace).
    :param overflow_indicator: The text that is appended if the text exceeds maximum_text_length.  Default '...'.
    :return: The generated text.
    """
    text = ""
    lastWord = None
    sentences = 0

    while len(text) < maximum_text_length:
        w = choose(d[lastWord])
        lastWord = w
        if w is None:
            if chance(chance_to_exit_when_sentence_terminates):
                break
            text += sentence_separator
            sentences += 1
        else:
            if len(text + w) > (maximum_text_length - len(overflow_indicator)):
                text = text[:-1] + overflow_indicator
                break
            else:
                text += w + " "

    return text
