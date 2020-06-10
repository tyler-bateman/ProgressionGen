from textgenrnn import textgenrnn

TEMPS = [0.3, 0.5, 1.0]

def main():
    textgen = textgenrnn('models/nn_weights.hdf5')
    for tmp in TEMPS:
        output = open('output/nn_chords_{}'.format(tmp), 'w')
        chords = textgen.generate(10, temperature = tmp)
        output.write(chords)
        

main()
