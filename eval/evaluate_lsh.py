"""
Usage: evaluate_lsh.py
Evaluate LSH algorithm performance with precision, recall, and f1 metrics
"""
from __future__ import division
from datasketch import MinHash
from nltk import ngrams
import utils
import os


def read_file(in_file, mode):
    """Read file"""
    if mode == 'char':
        filename, text = utils.read_file(in_file)
    elif mode == 'word':
        filename, text = utils.tokenize_file(in_file)
    return filename, text


def calculate_lsh(text, mode, lsh_type):
    """Calculate LSH for the file"""
    min_hash = MinHash(num_perm=128)
    if mode == 'char':
        for d in ngrams(text, 3):
            min_hash.update("".join(d).encode('utf-8'))
    elif mode == 'word':
        for d in ngrams(text, 3):
            min_hash.update(" ".join(d).encode('utf-8'))
    result = lsh_type.query(min_hash)
    return result


def eval_gold_tns(input_dir, mode, lsh_type):
    """
    Calculate LSHs for the files that do not contain plagiarism (tn_docs folder)
    Args:
        input_dir (str): directory to the files that do not contain plagiarism
                        (tn_docs folder)
        mode (str): type of ngrams to use ('char', 'word')
        lsh_type (MinHash object): previously calculated lsh
    Returns:
        tn: number of true negatives - files
            correctly marked as not plagiarized
        fp: number of false positives - files
            incorrectly marked as plagiarized
        writes names of the files to 'tn_log.txt'
        writes names of the files to 'fp.txt'
    """
    tn = fp = 0
    for f in os.listdir(input_dir):
        filename, text = read_file(os.path.join(input_dir, f), mode)
        result = calculate_lsh(text, mode, lsh_type)

        if len(result) > 0:
            fp += 1
            print "fp: ", filename, result
            with open('fp_log.txt', 'a+') as fp_log:
                fp_log.write('{0}\t{1}\n'.format(filename, result))
        else:
            tn += 1
            print 'tn: ', filename, result
            with open('tn_log.txt', 'a+') as tn_log:
                tn_log.write('{0}\n'.format(filename))
    return tn, fp


def eval_gold_tps(input_dir, mode, lsh_type):
    """Calculate LSHs for the files that contain plagiarism (tp_docs folder)
    Args:
        input_dir (str): directory to the files that contain plagiarism
                        (tp_docs folder)
        mode (str): type of ngrams to use ('char', 'word')
        lsh_type (MinHash object): previously calculated lsh
    Returns:
        tp: number of true positives - number of files
            correctly marked as plagiarized
        fn: number of false negatives - number of files
            incorrectly marked as not plagiarized
        writes names of the files to 'tp_log.txt'
        writes names of the files to 'fn.txt'
    """
    tp = fn = 0
    for f in os.listdir(input_dir):
        filename, text = read_file(os.path.join(input_dir, f), mode)
        result = calculate_lsh(text, mode, lsh_type)
        if len(result) == 0:
            fn += 1
            print "fn: ", filename, result
            with open('fn_log.txt', 'a+') as fn_log:
                fn_log.write('{0}\n'.format(filename))
        else:
            tp += 1
            print "tp: ", filename, result
            with open('tp_log.txt', 'a+') as tp_log:
                tp_log.write('{0}\t{1}\n'.format(filename, result))
    return tp, fn


def calculate_metrics(tn_directory, tp_directory, mode , lsh_type):
    """Calculate the results of the LSH algorithms performance"""
    tp, fn = eval_gold_tps(tp_directory, mode, lsh_type)
    tn, fp = eval_gold_tns(tn_directory, mode, lsh_type)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1, tp, tn, fp, fn


if __name__ == '__main__':
    tn_directory = '../data/golden/tn_docs/'
    tp_directory = '../data/golden/tp_docs/'


    # Evaluate lsh_word_05 model
    # lsh_word_05 = utils.load_lsh(utils.CACHE_WORD_05_FILE)
    # precision, recall, f1, tp, tn, fp, fn = calculate_metrics(tn_directory, tp_directory, 'word', lsh_word_05)
    # print 'lsh_word_05 evaluation:\nPrecision: {0}\nRecall: {1}\nF1 measure: {2}\nTPs: {3}\nTNs: {4}\nFPs: {5}\nFNs: ' \
    #       '{6}'.format(precision, recall, f1, tp, tn, fp, fn)
    # with open('word_05_eval_results.txt', 'w+') as out_file:
    #     out_file.write('Precision: {0}\nRecall: {1}\nF1 measure: {2}\nTPs: {3}\nTNs: {4}\nFPs: {5}\nFNs: ' \
    #       '{6}'.format(precision, recall, f1, tp, tn, fp, fn))

    # Evaluate lsh_char_03 model
    lsh_char_03 = utils.load_lsh(utils.CACHE_CHAR_03_FILE)
    precision, recall, f1, tp, tn, fp, fn = calculate_metrics(tn_directory, tp_directory, 'char', lsh_char_03)
    print 'lsh_char_03 evaluation:\nPrecision: {0}\nRecall: {1}\nF1 measure: {2}\nTPs: {3}\nTNs: {4}\nFPs: {5}\nFNs: ' \
          '{6}'.format(precision, recall, f1, tp, tn, fp, fn)
    with open('char_03_eval_results.txt', 'w+') as out_file:
        out_file.write('Precision: {0}\nRecall: {1}\nF1 measure: {2}\nTPs: {3}\nTNs: {4}\nFPs: {5}\nFNs: ' \
                       '{6}'.format(precision, recall, f1, tp, tn, fp, fn))

