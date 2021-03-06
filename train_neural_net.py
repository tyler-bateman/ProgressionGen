'''
This is the script for training the neural net. The neural net is trained on
16 epochs
'''

from textgenrnn import textgenrnn


def main():
    textgen = textgenrnn()
    textgen.reset()
    textgen.train_from_file('data/train_data.txt', num_epochs = 16)
    textgen.save('models/nn_weights.hdf5')

if __name__ == '__main__':
    main()
