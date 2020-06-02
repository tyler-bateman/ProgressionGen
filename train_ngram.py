

from math import log
from vocab import getVocab

START = (0, set())
END = (1, set())

def wrap(phrase, n):
    return [START for i in range(n - 1)] + phrase + [END]


def train(data, n, lmda):
    #Count the number of occurrences of each n-gram
    counts = {}
    v = getVocab(data)

    for phrase in data:
        p = wrap(phrase)
        for i in range(len(phrase) - n + 1):
            ngram = [p[j] for j in range(i, i + n)]
            context = ngram[:-1]
            token = ngram[-1]
            if context in counts:
                if token in counts[context]:
                    counts[context][token] += 1
                else:
                    counts[context][token] = 1
            else:
                counts[context] = {token : 1}

    prob = {}
    for context in counts:
        prob[context] = dict.fromkeys(v, log(lmda))
        total_count = 0
        for token in counts[context]:
            total_count += counts[context][token]

        total_count = log(total_count)
        for token in counts[context]:
            prob[context][token] += log(counts[context][token]) - total_count

    return prob
