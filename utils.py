# -*- coding: utf-8 -*-
"""
Collection of gloabl variables and functions that are used
(or may potentially be used) in different parts of the system
"""
import codecs
import pickle
from nltk.tokenize import word_tokenize

CACHE_CHAR_03_FILE = 'lsh_char_03.pickle'
# CACHE_CHAR_05_FILE = 'lsh_char_05.pickle'

CACHE_WORD_03_FILE = 'lsh_word_03.pickle'
CACHE_WORD_05_FILE = 'lsh_word_05.pickle'


def read_file(filename):
    """
    Read the file
    Returns:
        filename (str): the name of the file read
        text (str): text of the file as one string
    """
    with codecs.open(filename, 'r', 'utf-8') as in_file:
        text = in_file.read()
    return filename, text


def tokenize_file(filename):
    """
    Read and tokenize the file
    Returns:
        Returns:
        filename (str): the name of the file read
        token_text (list): list of tokenized words of the text
    """
    filename, text = read_file(filename)
    token_text = word_tokenize(text)
    return filename, token_text


def load_lsh(filename):
    """Load pickled lsh object"""
    with open(filename, 'rb') as handle:
        return pickle.load(handle)



