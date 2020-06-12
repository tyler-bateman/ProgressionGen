'''
Calculates the perplexity of the test data with the n-gram models.
'''


from nltk.util import ngrams
from nltk.lm.preprocessing import pad_both_ends

import dill as pickle

models = pickle.load(open('ngram_models.p', 'rb'))
test_data = open('data/test_data.txt', 'r').readlines()


def main():
    for i in range( len(models)):
        order = i + 1
        print('calculating ' + str(order) + '-gram perplexity...')
        p = 0
        model = models[i]
        for line in test_data:
            tokens = line.strip().split(' ')
            test_ngrams = list(ngrams(pad_both_ends(tokens, n = order), order))
            pp = model.perplexity(test_ngrams)
            p += pp
        print('{}-gram perplexity:'.format(order), p)

if __name__ == '__main__':
    main()
