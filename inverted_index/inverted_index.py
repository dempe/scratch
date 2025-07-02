import os
import re
import fileinput

punctuation_regex = r"[^\w\s]"


def normalize_tokens(tokens):
    """Remove all non-alphanumeric characters and convert to lower case"""
    tokens = [re.sub(punctuation_regex, "", token.lower()) for token in tokens]
    return tokens


def tokenize_input(user_input):
    """Split string on whitespace and return unique tokens"""
    tokens = normalize_tokens(user_input.split())
    return set(tokens)


def read_docs():
    """Read files in docs directory and return map of filename -> tokens in file"""
    docs_to_tokens = {}
    for filename in os.listdir("docs"):
        with open(os.path.join("docs", filename), 'r') as f:
            docs_to_tokens[filename] = tokenize_input(f.read())
    return docs_to_tokens


def make_index(docs):
    """Make inverted index of token -> docs containing token, number of docs containing token"""
    index = defaultdict()
    for doc in docs:
        for token in docs[doc]:
            if token not in index:
                index[token] = {}
                index[token]['count'] = 0
                index[token]['docs'] = []
            index[token]['count'] += 1
            index[token]['docs'].append(doc)
    return index


def query_index(key, index):
    """Return docs that contain key"""
    if key not in index:
        return None
    return index[key]['docs']


def main():
    index = make_index(read_docs())
    for line in fileinput.input():
        print(query_index(line.rstrip(), index))


if __name__ == "__main__":
    main()
