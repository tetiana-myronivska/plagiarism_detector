# Comments

## Project workflow
 1. Research existing approaches to plagiarism detection:
    - Substring matching
    - Text parsing
    - Fingerprinting
    - Bag Of Words Analysis
    - Stylometry
    - Citation-based
2. Check ready solutions and their metrics
   - Turnitin
   - Grammarly
   - Search Engine Reports.
3. Set key requirements:
   - Speed
   - Scalability.
4. Devise evaluation metrics:
   - Precision
   - Recall.
5.  Choose algorithm: Locality Sensitive Hashing.
6. Find data: PAN-PC-09 corpus (used for the evaluation of automatic plagiarism detection algorithms, [link](https://www.uni-weimar.de/en/media/chairs/computer-science-and-media/webis/corpora/corpus-pan-pc-09/))
7. Design the system.
8. Preprocess the data.
9. Implement algorithm.
10. Implement evaluation tests.
11. Evaluate the system.
12. Define next steps.


 ## Algorithm rationale
The algorithm chosen for this task is fingerprinting with Locality Sensitive Hashing (LSH, [link](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)). The main idea of LSH lies in calculating and saving hash values for each document in the existing database. The incoming document that has to be checked for plagiarism also gets its hash value, and this value is then queried in LSH object. If there is a collision between the new hash and existing hashes, the document is plagiarized.

 Such choice of algorithm is determined by the key requirements, which are speed and scalability: the LSH values are calculated only once for each of the documents in the database.


## Data choice and preprocessing
For creating the database of the documents, a part of PAN-PC-09 corpus ([link](https://www.uni-weimar.de/en/media/chairs/computer-science-and-media/webis/corpora/corpus-pan-pc-09/)) has been used. The corpus was initially created for the evaluation of automatic plagiarism detection algorithms. It can be used free of charge for research purposes.

The subset of the original corpus has been preprocessed by parsing the xml annotations of the source .txt files (See [README.md](README.md) for the structure of the **data** folder).


## First results
|Metrics | Models
|-----   | ----------------- |
|        | **3_char_0.5_thresh** |
|TP| 50|
|TN| 1|
|FP| 49|
|FN| 0|
| Precision| 0.505 |
| Recall | 1.0 |
| F1    | 0.6711 |



Currently, the system is calculating Precision, Recall and F1-measure for different variants of LSH.

## Additional questions
1. How would you assess the performances of your system?
 At this moment, the system is quite raw. It needs algorithm quality improvement, a lot of refactoring, and UI implementation. [Next steps](#next-steps) have been defined for further work on the system.
2. How could malicious authors potentially fool your system?
The system is not robust against plagiarism with paraphrasing. To address this problem, semantic features can be added to LSH (e.g., TF-IDF).
Also, its Precision and Recall of the system depend heavily on the choice of the threshold parameter chosen for the database, which is

3. Is your system scalable w.r.t. number of documents / users? If not, how would address the
scalability (in terms of algorithms, infrastructure, or both)?

## Next steps
1. Improve the LSH quality:
   - Choose optimal threshold and ngrams through experiments.
   - Experiment with data preprocessing by removing punctuation, stop words, and stemming.
- Refactor the system.
- Implement UI.
- Update documentation with Sphinx.
- Implement feature for adding the LSH of the newly checked document to the database.
- Implement more detailed evaluation: include the evaluation of the source documents detected in plagiarized documents.
- Implement detection of plagiarized parts of the text.
 **Idea:** use the output of LSH and implement the Longest Common Substring matching algorithm for the the pairs of documents detected as plagiarized by the original LSH.
6. Add domain-specific feature (if needed): take into account scientific papers and treat citations differently in terms of plagiarism.
