import pickle, math


def ivlToString(ivl):
    return 'E' if ivl == 11 else 'T' if ivl == 10 else str(ivl)

def parse(data):
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
    train_size = math.floor(len(data) * 0.80)
    train_output.writelines(all_data[:train_size])
    test_output.writelines(all_data[train_size:])

if __name__ == '__main__':
    main()
