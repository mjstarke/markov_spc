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


def superstrip(a):
    if a is None:
        return None
    simple = a
    for garbage in [".", "...", "?", "!", "(", ")", ","]:
        simple = simple.replace(garbage, "")
    return simple.lower()


def read_paragraphs(fp, delete):
    """
    Reads a text file as a sequence of paragraphs.
    :param fp: The path to the text file.
    :param delete: Strings that should be deleted from the text.
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


def create_superdict(paragraphs):
    """
    Creates the superdictionary from the given paragraphs.
    :param paragraphs: The paragraphs.
    :return: The superdictionary.
    """
    d = dict()
    # alias = dict()
    # null = False
    firstPara = randint(0, len(paragraphs) - PARAGRAPHS_TO_USE)

    for para in paragraphs[firstPara:(firstPara + PARAGRAPHS_TO_USE)]:
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


def generate_tweets(d):
    """
    Generates tweets using the given superdictionary.
    :param d: The superdictionary.
    :return: A list of tweets.
    """
    tweets = []
    for t in range(TWEETS_TO_GENERATE):
        tweet = ""
        lastWord = None
        sentences = 0

        while len(tweet) < MAXIMUM_TWEET_LENGTH:
            # choices = []
            # for al in alias[superstrip(lastWord)]:
            #     choices += d[al]

            w = choose(d[lastWord])
            lastWord = w
            if w is None:
                if chance(CHANCE_TO_EXIT_AFTER_SENTENCE_TERMINATES):
                    break
                tweet += " " if DOUBLE_SPACE_BETWEEN_SENTENCES else ""
                sentences += 1
            else:
                if len(tweet + w) > (MAXIMUM_TWEET_LENGTH - 3):
                    tweet = tweet[:-1] + "..."
                    break
                else:
                    tweet += w + " "
        print(tweet)
        print()
        tweets.append(tweet)

    return tweets
