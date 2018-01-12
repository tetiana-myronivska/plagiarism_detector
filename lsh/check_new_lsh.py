# -*- coding: utf-8 -*-
"""
Usage: check_new_lsh.py
Check new document for plagiarism
"""
from datasketch import MinHash
from nltk import ngrams
import utils

lsh = utils.load_lsh(utils.CACHE_WORD_03_FILE)
# lsh = utils.load_lsh(utils.CACHE_CHAR_03_FILE)
# lsh = utils.load_lsh(utils.CACHE_CHAR_04_FILE)
# lsh = utils.load_lsh(utils.CACHE_CHAR_05_FILE)




def check_new_lsh(filename):
    """Read input file, calculate its LSH
        and query it in the LSH database

        Returns:
            empty list [] - the file is not plagiarized (no LSH collision)
            list [source_filenames] - list with file names of sources of plagiarism
            """
    filename, text = utils.tokenize_file(filename)
    min_hash = MinHash(num_perm=128)

    for d in ngrams(text, 3):
        min_hash.update(" ".join(d).encode('utf-8'))

    return lsh.query(min_hash)


if __name__ == '__main__':
    check_file = 'test_suspicious.txt'
    result = check_new_lsh(check_file)
    if len(result) == 0:
        print "The document is not plagiarized"
    else:
        print "The document is plagiarized.\n" \
              "Here is the list of the files that were used:\n{}".format(result)
    # TODO:
    # Add argparse for providing file name with script call