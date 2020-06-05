# The following information about chords will be stored. Any chord that has the
# same information will be assumed to be the same chord.
# 1. The bass note of the chord, i.e. the lowest note.
#      An integer from 0 (corresponding to 'C') to 11 (corresponding to 'B')
# 2. A list of intervals in half-steps between the bass note and the other notes in the chord
#        - Any repeated notes will be ignored
#        - All notes will be octave-shifted to the single actave above the bass note
#        - Thus, all values in the list will be a number from 1-11
#
#
# Chords will be sampled from the data at 4 every 250 ms, which is 16th notes
# at the interonset interval that Westergaard calls 'too fast to be useful'. I
# figure that it is unlikely that any chordal information would be skipped at
# that rate.
# Of course, most chords will last longer than 250 ms. Because this task relates
# to the transitions between chords, any time a chord is identical to the
# preceding chord (according the the rules above), it will be ignored.
#
# Because this task relates to chords, single melody lines will also be ignored.
# For my purposes, any time there is greater than 2 seconds betwen chords, be it
# because of a rest or a period of unaccompanied melody (including multiple
# instruments playing in unison), the next chord of two or more notes will be
#   considered the start of a new phrase.

import numpy as np, pickle
from intervaltree import Interval, IntervalTree

#Audio samples per second
fs = 44100

#Samples per chord
spc = fs // 16

#Retrieve training data
train_data = np.load(open('musicnet.npz', 'rb'), allow_pickle = True, encoding = 'latin1')

#Retain a list of all MusicNet IDs
ids = list(train_data.keys())


#Converts the chord into a format that is hashable
#Param chord: (bass, deltas) where bass is an int and deltas is a set of ints
def hashable(chord):
    return(chord[0], tuple(chord[1]))



# Returns a tuple: (bass, deltas)
# bass: an integer from 0 to 11 representing it's relation to the previous bass note
# deltas: A set containing integers representing the distance in semitones from
#         the bass note to each other note in the chord, normalized to one octave
def normalizeChord(interval, prevBass):
    notes = [label[2][1] for label in sorted(interval)]
    bass = (notes.pop(0) - prevBass) % 12
    deltas = set([(note - bass) % 12 for note in notes])
    deltas.discard(0)
    return (bass, deltas)


# Returns a list of lists of chords in the order that they appear in the piece
# Sequences of chords are diveded into phrases, which for these purposes wll
# be delimited by 2 seconds since the last chord.
# Each chord is of the format specified by normalizeChord above
# A chord must meet two criteria in order to
def getChords(id):
    phrases = []
    chords = []
    labels = train_data[id][1]
    moment = labels.begin()
    prevTime = labels.begin()
    while moment < labels.end():
        if len(labels[moment]) > 1:
            prevChord = chords[-1] if len(chords) > 0 else (0, set([]))
            chord = normalizeChord(labels[moment], prevChord[0])
            if len(chord[1]) > 0 and (chord[0] != prevChord[0] or not chord[1].issubset(prevChord[1])):
                if prevChord[0] == chord[0] and prevChord[1].issubset(chord[1]):
                    prevChord[1].update(chord[1])
                else:
                    if (moment - prevTime) / fs > 2:
                        phrases.append(chords)
                        chords = []
                        prevTime = moment
                    chords.append(chord)
        moment += spc
    phrases.append(chords)
    return phrases

# Returns a list of all musical phrases in MusicNet
def getAllPhrases():
    phrases = []
    for id in train_data:
        print('getting chords for', id)
        phrases += getChords(id)
    return phrases


# Parses and pickles the training data
def main():
    data = getAllPhrases()
    pickle.dump(data, open('parsed_data.p', 'wb'))


if __name__ == '__main__':
    main()
