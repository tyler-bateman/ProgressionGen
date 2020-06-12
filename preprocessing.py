import pickle, math

"""
The methods in this file turn the parsed dataset into a format that can be
accepted by pre-packaged language models.
It also splits the dataset into training data and test data.
"""

def ivlToString(ivl):
    """
    Returns the character representation of a pitch class or interval
    """
    return 'E' if ivl == 11 else 'T' if ivl == 10 else str(ivl)

def parse(data):
    """
    Formats each phrase as a string, returns a list of strings.
    """
    phrases = []
    for p in data:
        tokens = ['0'] + [ivlToString(t) for t in p[0]]
        for i in range(len(tokens)):
            for ivl in p[1][i]:
                tokens[i] += ivlToString(ivl)
        phrases.append(' '.join(tokens) + '\n')
    return phrases

def main():
    data = pickle.load(open('data/parsed_data.p', 'rb'))
    train_output = open('data/train_data.txt', 'w')
    test_output = open('data/test_data.txt', 'w')
    all_data = parse(data)
    train_size = math.floor(len(data) * 0.99)
    train_output.writelines(all_data[:train_size])
    test_output.writelines(all_data[train_size:])

if __name__ == '__main__':
    main()
