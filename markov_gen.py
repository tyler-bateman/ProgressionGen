import markovify
from chordstomidi import write_file


def main():
    for order in range(1, 4):
        with open('models/{}-order_markov.txt'.format(order), 'r') as f:
            model = markovify.Text.from_json(f.readline())
        with open('output/{}-order_markov_chords.txt'.format(order), 'w') as output:
            for i in range(10):
                seq = model.make_sentence().strip()
                print(seq)
                output.write(seq)
                write_file('midi_files/{}-order_markov_{}.mid'.format(order, i), seq.split(' '))

if __name__ == '__main__':
    main()
