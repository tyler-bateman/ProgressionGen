"""
Calculates the average scores for each model given the human evaluations.
"""

import os

model_types = ['1-gram', '2-gram', '3-gram', '4-gram', '1-order_markov', '2-order_markov', '3-order_markov', 'nn_0.5', 'nn_0.75', 'nn_1.0']

evals = os.listdir('evals')
with open('human_eval_files.txt', 'r') as f:
    filenames = [name.strip() for name in f.readlines()]

def calculateScores():
    counts = dict.fromkeys(set(model_types), 0)
    for eval in evals:
        with open('evals/{}'.format(eval), 'r') as f:
            scores = [s.strip() for s in f.readlines()]
        for i in range(len(filenames)):
            for type in model_types:
                if type in filenames[i]:
                    counts[type] += int(scores[i])
    scores = {}
    for item in counts.items():
        scores[item[0]] = item[1] / (len(evals) * 4)
    return scores



def main():
    scores = calculateScores()
    for item in scores.items():
        print(item)

if __name__ == '__main__':
    main()
