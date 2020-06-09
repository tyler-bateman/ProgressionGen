from textgenrnn import textgenrnn


def main():
    textgen = textgenrnn('models/nn_weights.hdf5')
    textgen.generate_samples()
