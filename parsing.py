"""
The following information about chords will be parsed from the dataset. Any
chord that has the same information will be assumed to be the same chord.
1. The bass note of the chord, i.e. the lowest note.
     An integer from 0 (corresponding to 'C') to 11 (corresponding to 'B')
2. A list of intervals in half-steps between the bass note and the other notes in the chord
       - Any repeated notes will be ignored
       - All notes will be octave-shifted to the single actave above the bass note
       - Thus, all values in the list will be a number from 1-11


Chords will be sampled from the data at 4 every 250 ms, which is sixteenth notes
at the interonset interval that Westergaard calls 'too fast to be useful'. I
figure that it is unlikely that any significant chordal information would be
skipped at that rate.
Of course, most chords will last longer than 250 ms. Because this task relates
to the transitions between chords, any time a chord is identical to the
preceding chord (according the the rules above), it will be ignored.

Any time there is a moment of silence, this will be treated as a break between
phrases.
"""

import numpy as np, pickle
from intervaltree import Interval, IntervalTree

#Audio samples per second
fs = 44100

#Samples per chord
spc = fs // 16

#Retrieve training data
train_data = np.load(open('data/musicnet.npz', 'rb'), allow_pickle = True, encoding = 'latin1')


# Returns a tuple: (bass, deltas)
# bass: an integer from 0 to 11 representing the pitch class of the lowest note
# deltas: A set containing integers representing the distance in semitones from
#         the bass note to each other note in the chord, normalized to one octave
def normalizeChord(interval):
    notes = [label[2][1] for label in interval]
    notes = sorted(notes)
    bass = notes.pop(0) % 12
    deltas = set([(note - bass) % 12 for note in notes])
    deltas.discard(0)
    deltas = tuple(sorted(deltas))
    return (bass, deltas)



def getChords(id):
    """
    Returns a lists of chords qualities in the order that they appear in the piece
    and a list of transition intervals for the bass notes
    Sequences of chords are diveded into phrases, which for these purposes wll
    be delimited by 2 seconds since the last chord.
    Each chord is of the format specified by normalizeChord above
    """
    labels = train_data[id][1]

    phrases = []

    qualities = []
    transitions = []
    durations = []


    moment = labels.begin()
    prevBass = None
    prevQuality = None
    #Parse individual chords
    while moment < labels.end():

        if len(labels[moment]) > 0:
            c = normalizeChord(labels[moment])
            if prevBass != c[0] or prevQuality != c[1]:
                if len(qualities) > 0:
                    transitions.append((c[0] - prevBass) % 12)
                qualities.append(c[1])
                prevBass = c[0]
                prevQuality = c[1]
        else:
            if len(transitions) > 0:
                phrases.append((transitions, qualities))
            qualities = []
            transitions = []

        moment += spc

    return phrases



def getAllPhrases():
    """
    Returns a list of all musical phrases in MusicNet
    """
    phrases = []
    for id in train_data:
        print('getting chords for', id)
        phrases += getChords(id)
    return phrases



def main():
    """
    Parses and pickles the training data
    """
    data = getAllPhrases()
    pickle.dump(data, open('data/parsed_data.p', 'wb'))


if __name__ == '__main__':
    main()
