# -*- coding: utf-8 -*-
"""
Usage: preprocess_raw_data.py
Preprocess raw data:
- parse .txt files and their .xml annotations
- write files with original (not plagiarized) text to tn_docs floder
- write files with plagiarized text to tp_docs folder,
together with the sources of plagiarism
"""
try:
    import xml.etree.cElementTree as ET

except ImportError:
    import xml.etree.ElementTree as ET

import os
from shutil import copyfile


TRUE_NEGATIVE_FOLDER = 'tn_docs'
TRUE_POSITIVE_FOLDER = 'tp_docs'


def split_suspicious(input_dir):
    """Split the directory with suspicious files into true_negatives and true_positives"""
    for filename in os.listdir(input_dir):
        if filename.endswith('.xml'):
            with open(os.path.join(input_dir, filename)) as file:
                parse_file(file)


def parse_file(file):
    """Parse each file in the directory"""
    doc = ET.parse(file)

    # Choose only documents with the English language
    for el in doc.findall(".//feature[@name='language']"):
        lang = el.attrib['value']
        if lang != "en":
            return

    ap_len = len(doc.findall(".//feature[@name='artificial-plagiarism']"))

    # Sort out original and plagiarized texts
    if ap_len == 0:
        copy_file(TRUE_NEGATIVE_FOLDER, file.name)
    else:
        process_ap_features(file, doc)


def process_ap_features(file, doc):
    """Parse .xml files, extract features, and write the results to files"""
    features = doc.findall(".//feature[@name='artificial-plagiarism'][@translation='false'][@obfuscation='none']")
    uniq_sr = set()

    for el in features:
        uniq_sr.add(el.attrib['source_reference'])

    if len(uniq_sr) > 0:
        copy_file(TRUE_POSITIVE_FOLDER, file.name)
        save_to_file(TRUE_POSITIVE_FOLDER, file.name, uniq_sr)


def copy_file(folder, file_name):
    """Copy files with plagiarized text to tp_docs folder"""
    path = os.path.splitext(file_name)[0]
    name = path.split('/')[3]
    dist = folder + '/' + name + '.txt'
    copyfile(path + '.txt', dist)


def save_to_file(folder, file_name, content):
    """Write source references for plagiarized document to file"""
    path = os.path.splitext(file_name)[0]
    name = path.split('/')[3] + '-sr'
    save_path = os.path.join(folder, name + ".txt")

    new_file = open(save_path, "w")
    new_file.write('\n'.join(content))
    new_file.close()


if __name__ == '__main__':
    directory = './raw/suspicious_documents/'
    split_suspicious(directory)
