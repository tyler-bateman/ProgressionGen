# This file contains various useful language modeling tools common between
# different language models

import pickle

from ngram import START, END

# data: as generated by parsing.py
def getVocab(data):
    v = set([tuple(sorted(item[1])) for item in data] + [START, END])
    return v

#generates and pickles the vocabulary
def main():
    data = pickle.load(open('parsed_data.p', 'rb'))
    vocab = getVocab(data)
    print(len(vocab), 'unique chords')
    pickle.dump(vocab, open('vocab.p', 'wb'))

if __name__ == '__main__':
    main()
