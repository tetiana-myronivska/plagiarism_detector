# plagiarism_detector
This is a plagiarism detection tool built using the locality sensitive hashing (LSH) algorithm with minhash.

The tool uses Python `datasketch` library for calculating `MinHash` and `MinHashLSH`.

## Prerequisites
**NLTK package**
```python
sudo pip install -U nltk
python  
import nltk  
nltk.download() # Here, choose the package *popular*. It contains all the necessary packages.
```

**datasketch**  
```
pip install datasketch -U
```

**redis**  
*Note:* redis server is only needed for recalculation of LSH for the whole document collection.
```python
# Install redis:
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
# Start your redis:
$ redis-server
# Check if your redis server is running:
$ redis-cli ping
# Expected response: PONG
```

## Usage
Open the project. In `lsh/check_new_lsh.py` script specify `check_file` for the file to be checked for plagiarism, and run the script. Output: message about whether the document is plagiarized or not. If the document is plagiarized, the list of source document names is printed.

## Project structure
`data` - folder with data files. Subfolders and files:
  - `golden` - documents retrieved from the `raw` folder: `tn_docs` - folder with files that are not plagiarized (true negatives); `tp_docs` - folder with files that are plagiarized (true positives); `tp_source_references` - folder with files that contain source references for plagiarized files
  - `raw` - part of the original PAN-PC-09 corpus corpus, [link](https://www.uni-weimar.de/en/media/chairs/computer-science-and-media/webis/corpora/corpus-pan-pc-09/))
  - `preprocess_data.py` - script for preprocessing files in the `raw` folder.

`eval` - folder with evaluation script and precomputed variants of LSH for the document database.

`lsh` - folder with the script for calculating LSH for the document database and precomputed variants of LSH. Also contains `check_new_lsh.py` script for checking new document for plagiarism.

`utils.py` - file with useful functions and global variables that are (or may potentially be) in different parts of the project.

`COMMENTS.md` - file with commets to the project and answers to the additional questions.
