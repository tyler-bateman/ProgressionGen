

from math import log
from vocab import getVocab, START, END
import random, pickle



def wrap(phrase, n):
    return [START for i in range(n - 1)] + phrase + [END]


def train(data, n, lmda):
    #Count the number of occurrences of each n-gram
    counts = {}
    v = getVocab(data)

    for phrase in data:
        p = wrap(phrase, n)
        for i in range(len(phrase) - n + 1):
            ngram = [(p[j][0], tuple(sorted(p[j][1]))) for j in range(i, i + n)]
            context = tuple(ngram[:-1])
            token = tuple(ngram[-1])
            if context in counts:
                if token in counts[context]:
                    counts[context][token] += 1
                else:
                    counts[context][token] = 1
            else:
                counts[context] = {token : 1}

    # Find the log probabilities for each ngram
    prob = {}
    for context in counts:
        prob[context] = dict.fromkeys(v, log(lmda))
        total_count = 0
        for token in counts[context]:
            total_count += counts[context][token]

        total_count = log(total_count + (len(v) * lmda))
        for token in counts[context]:
            print('context:', context)
            print('token:', token)
            print(token in v)
            prob[context][token] += log(counts[context][token]) - total_count

    return prob

def generateChords(model, v):
    vList = list(v)
    n = len(list(model.keys())[0]) + 1
    prog = [START for i in range(n - 1)]
    nextChord = START

    while nextChord != END:
        context = tuple(prog[1 - n:])
        nextChord = random.choices(vList, weights = [model[context][t] for t in vList])
        prog.append(nextChord)

    return prog

def main():
    data = pickle.load(open('parsed_data.p', 'rb'))
    model = train(data, 3, 0.001)
    prog = generateChords(model, getVocab(data))
    print(prog)

main()
