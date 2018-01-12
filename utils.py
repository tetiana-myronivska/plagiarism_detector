import codecs
from nltk.tokenize import word_tokenize

CACHE_CHAR_03_FILE = 'lsh_char_03.pickle'
CACHE_CHAR_05_FILE = 'lsh_char_05.pickle'

CACHE_WORD_03_FILE = 'lsh_word_03.pickle'
CACHE_WORD_05_FILE = 'lsh_word_05.pickle'


def read_file(filename):
    with codecs.open(filename, 'r', 'utf-8') as in_file:
        text = in_file.read()
    return filename, text


def tokenize_file(filename):
    filename, text = read_file(filename)
    token_text = word_tokenize(text)
    return filename, token_text



