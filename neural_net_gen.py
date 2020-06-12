'''
Uses trained neural net to generate 10 lines of chords in strings of at most 50 chords
Chords are generated at temperatures of 0.5, 0.75, and 1.0
'''

from textgenrnn import textgenrnn
from chordstomidi import write_file

TEMPS = [0.5, 0.75, 1.0]

def main():
    textgen = textgenrnn('models/nn_weights.hdf5')
    for tmp in TEMPS:
        filename = 'output/nn_chords_{}.txt'.format(tmp)
        textgen.generate_to_file(filename, n = 10, temperature = tmp)
        progs = open(filename, 'r').readlines()
        for i in range(len(progs)):
            p = progs[i].strip().split(' ')
            write_file('midi_files/nn_{}_{}.mid'.format(tmp, i), p)


main()
