from random import choice as choose
from random import random as r
from random import randint

CHANCE_TO_EXIT_AFTER_SENTENCE_TERMINATES = randint(25, 50)
DOUBLE_SPACE_BETWEEN_SENTENCES = True
MAXIMUM_TWEET_LENGTH = randint(randint(150, 275), 280)
PARAGRAPHS_TO_USE = randint(10, 30)
STRINGS_TO_DELETE_FROM_CORPUS = ["\n", "SUMMARY...", "DISCUSSION..."]
TWEETS_TO_GENERATE = 10


def chance(c):
    """
    Returns True with the given probability, and False otherwise.
    :param c: The chance to return True out of 100.
    :return: True or False randomly.  Always True if c >= 100, and always False if c <= 0.
    """
    return c / 100. > r()


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
        while True:
            try:
                words.remove("")
            except:
                break

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


def generate_text(d):
    """
    Generates text using the given superdictionary.
    :param d: The superdictionary.
    :return: The generated text.
    """
    text = ""
    lastWord = None
    sentences = 0

    while len(text) < MAXIMUM_TWEET_LENGTH:
        # choices = []
        # for al in alias[superstrip(lastWord)]:
        #     choices += d[al]

        w = choose(d[lastWord])
        lastWord = w
        if w is None:
            if chance(CHANCE_TO_EXIT_AFTER_SENTENCE_TERMINATES):
                break
            text += " " if DOUBLE_SPACE_BETWEEN_SENTENCES else ""
            sentences += 1
        else:
            if len(text + w) > (MAXIMUM_TWEET_LENGTH - 3):
                text = text[:-1] + "..."
                break
            else:
                text += w + " "

    return text
