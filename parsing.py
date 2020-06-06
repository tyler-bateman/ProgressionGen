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



# Returns a tuple: (bass, deltas)
# bass: an integer from 0 to 11 representing the pitch class of the lowest note
# deltas: A set containing integers representing the distance in semitones from
#         the bass note to each other note in the chord, normalized to one octave
def normalizeChord(interval):
    notes = [label[2][1] for label in sorted(interval)]
    bass = notes.pop(0) % 12
    deltas = set([(note - bass) % 12 for note in notes])
    deltas.discard(0)
    return (bass, deltas)


# Returns a lists of chords qualities in the order that they appear in the piece
# and a list of transition intervals for the bass notes
# Sequences of chords are diveded into phrases, which for these purposes wll
# be delimited by 2 seconds since the last chord.
# Each chord is of the format specified by normalizeChord above
def getChords(id):
    labels = train_data[id][1]

    qualities = []
    transitions = []
    durations = []


    moment = labels.begin()
    prevChord = None

    #Parse individual chords
    while moment < labels.end():
        c = None
        if len(labels[moment]) > 0:
            c = normalizeChord(labels[moment])
            if c != prevChord:
                q = c[1]
                t = ((c[0] - (transitions[-1] if len(transitions) > 0 else 0)) + 12) % 12
                if not prevChord is None and t == 0 and q.issubset(prevChord[1]):
                    durations[-1][1] = moment
                elif not prevChord is None and t == 0 and q.issuperset(prevChord[1]):
                    qualities[-1] = q
                    durations[-1][1] = moment
                else:
                    qualities.append(q)
                    transitions.append(t)
                    durations.append([moment, moment])
            else:
                durations[-1][1] = moment

        moment += spc
        prevChord = c

    #remove non-chords and convert qualities to tuples
    idx = 0
    while idx < len(qualities):
        qualities[idx] = tuple(sorted(qualities[idx]))
        if len(qualities[idx]) == 0:
            qualities.pop(idx)
            durations.pop(idx)
            transitions.pop(idx)
            idx -= 1

        idx += 1

    #Split into phrases
    phrases = []
    startIndex = 0
    for i in range(len(qualities) - 1):
        if durations[i + 1][0] - durations[i][1] > fs * 2:
            phrases.append((transitions[startIndex + 1 : i + 1], qualities[startIndex : i + 1]))
            startIndex = i + 1

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
    print(data[0])
    pickle.dump(data, open('parsed_data.p', 'wb'))


if __name__ == '__main__':
    main()
