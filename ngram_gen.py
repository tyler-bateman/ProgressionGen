import dill as pickle


def generate_chord_sequence(num, model):
    return model.generate(50)

def main():
    models = pickle.load(open('ngram_models.p', 'rb'))
    for i in range(len(models)):
        print(str(i + 1) + '-gram chords:')
        print(generate_chord_sequence(100, models[i]))
main()
