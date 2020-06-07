import dill as pickle
import chordstomidi as midi

def generate_chord_sequence(num, model):
    return model.generate(50)

def main():
    models = pickle.load(open('ngram_models.p', 'rb'))
    for i in range(len(models)):
        output = open('output/{}-gram_chords.txt'.format(i+1), 'w')
        for j in range(20):
            chords = generate_chord_sequence(60, models[i])
            midi.write_file('midi_files/{}-gram_{}.mid'.format(i+1, j), chords)
            output.write(' '.join(chords) + '\n')

main()
