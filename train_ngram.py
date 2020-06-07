from nltk.util import ngrams
from nltk.util import everygrams
from nltk.lm.preprocessing import padded_everygram_pipeline as pep
from nltk.lm import MLE
import dill as pickle


def trainModel(n, lines):
    ngrams, phrases = pep(n, lines)
    model = MLE(n)
    model.fit(ngrams, phrases)
    return model

def main():
    #Generate ngram models from unigrams to quadrigrams
    input = open('data/train_data.txt', 'r')
    train_data = [line.strip().split() for line in input.readlines()]
    models = [trainModel(n, train_data) for n in range(1, 5)]
    pickle.dump(models, open('ngram_models.p', 'wb'))

main()
