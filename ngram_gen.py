'''
Uses trained ngram models to generate 10 lines of chords in strings of at most 50 chords
'''


import dill as pickle
import chordstomidi as midi

def main():
    models = pickle.load(open('models/ngram_models.p', 'rb'))
    for i in range( len(models)):
        model = models[i]
        output = open('output/{}-gram_chords.txt'.format(i+1), 'w')
        for j in range(10):
            print(j)
            chords = model.generate(50)
            midi.write_file('midi_files/{}-gram_{}.mid'.format(i+1, j), chords)
            output.write(' '.join(chords) + '\n')

if __name__ == '__main__':
    main()
