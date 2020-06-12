"""
Provides functionality to convert sequences of chords in string format into midi files
"""

from mxm.midifile import MidiOutFile

T = 48
V = 64


def str_p(p):
    """
    Converts the character format of a note into its respective pitch class
    """
    return 11 if p == 'E' else 10 if p == 'T' else int(p)

def str_to_pitches(chord, prevBass):
    """
    Converts the string format of a chord into its pitch classes.
    """
    if chord == '<s>' or chord == '</s>':
        return []
    else:
        bass = (str_p(chord[0]) + prevBass) % 12 + T
        cts = [bass + str_p(n) for n in chord[1:]]
        return [bass] + cts


def write_file(filename, chords):
    """
    Writes a midi file of the given file name from the list of chords given.
    """
    midi = MidiOutFile(open(filename, 'wb'))
    midi.header(format = 0, nTracks = 12, division = 16)
    midi.start_of_track()
    time = 0
    prevBass = 0
    prevChord = []
    for i in range(len(chords)):
        c = str_to_pitches(chords[i], prevBass)
        nextChord = [] if i + 1 >= len(chords) else str_to_pitches(chords[i + 1], c[0] if len(c) > 0 else 0)
        for n in c:
            if n not in prevChord:
                midi.update_time(time, relative = False)
                midi.note_on(0, n, V)
        time += 8
        for n in c:
            if n not in nextChord:
                midi.update_time(time, relative = False)
                midi.note_off(0, n, V)
        prevBass = c[0] if len(c) > 0 else 0
        prevChord = c
    midi.update_time(0)
    midi.end_of_track()
