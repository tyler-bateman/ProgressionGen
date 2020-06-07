from nltk.util import ngrams
from nltk.util import everygrams
from nltk.lm.preprocessing import padded_everygram_pipeline as pep
from nltk.lm import MLE
import dill as pickle
import math


def trainModel(n, lines):
    ngrams, phrases = pep(n, data)
    model = MLE(n)
    model.fit(ngrams, phrases)
    return model

def main():
    #Generate ngram models from unigrams to quadrigrams
    input = open('parsed_data.txt', 'r')
    data = [line.strip().split() for line in input.readlines()]
    train_size = math.floor(len(data) * 0.80)
    train_data = data[:train_size]
    models = [trainModel(n, train_data) for n in range(1, 5)]
    pickle.dump(models, open('ngram_models.p', 'wb'))

main()
