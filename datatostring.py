import pickle


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
    data = pickle.load(open('parsed_data.p', 'rb'))
    output = open('parsed_data.txt', 'w')
    output.writelines(parse(data))

if __name__ == '__main__':
    main()
