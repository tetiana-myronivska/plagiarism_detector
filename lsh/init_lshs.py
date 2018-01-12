# -*- coding: utf-8 -*-
"""
Usage: init_lshs.py
Initialize, calculate, and pickle LSH for the document database
"""
from datasketch import MinHash, MinHashLSH
import os
import pickle
import nltk
import utils


def init_lshs(directory, type, threshold):
    """Initilize and calculate LSH for the document database

    Args:
        directory (str): the directory with source files
        type (str): type of ngrams to use ('char', 'word')
        threshold (float): Jaccard threshold value

    Returns:
        lsh: datasketch object
    """
    # Create a MinHashLSH index using Redis as the storage layer
    lsh = MinHashLSH(threshold=threshold, num_perm=128,
                     storage_config={'type': 'redis', 'redis': {'host': 'localhost', 'port': 6379, 'db': 1},
                                     'name': 1})

    data_list = []

    for f in os.listdir(directory):
        minhash = MinHash(num_perm=128)
        if type == 'char':
            filename, text = utils.read_file(os.path.join(directory, f))
            print filename
            for d in nltk.ngrams(text, 3):
                minhash.update("".join(d).encode('utf-8'))
        elif type == 'word':
            filename, text = utils.tokenize_file(os.path.join(directory, f))
            print filename
            for d in nltk.ngrams(text, 3):
                minhash.update(" ".join(d).encode('utf-8'))

        data_list.append((filename, minhash))

    with lsh.insertion_session() as session:
        for key, minhash in data_list:
            session.insert(key, minhash)

    return lsh


def serialize(lsh_type, cache_file):
    """Pickle lsh object"""
    with open(cache_file, 'wb') as handle:
        pickle.dump(lsh_type, handle)


if __name__ == '__main__':
    lsh_word_03 = init_lshs('../data/raw/source_documents/', 'word', 0.3)
    serialize(lsh_word_03, utils.CACHE_WORD_03_FILE)
    # TODO:
    # serialize(lsh_char_03, utils.CACHE_CHAR_03_FILE)
    # serialize(lsh_char_05, utils.CACHE_CHAR_05_FILE)
    # lsh_char_03 = init_lshs('../data/raw/source_documents/', 'char', 0.3)
    # lsh_char_05 = init_lshs('../data/raw/source_documents/', 'char', 0.5)
