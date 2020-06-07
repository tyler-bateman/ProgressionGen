from mxm.midifile import MidiOutFile

T = 48
V = 64


def str_p(p):
    return 11 if p == 'E' else 10 if p == 'T' else int(p)

def str_to_pitches(chord, prevBass):
    bass = (str_p(chord[0]) + prevBass) % 12 + T
    cts = [bass + str_p(n) for n in chord[1:]]
    return [bass] + cts


def write_file(filename, chords):
    midi = MidiOutFile(open(filename, 'wb'))
    midi.header(format = 0, nTracks = 12, division = 16)
    midi.start_of_track()
    time = 0
    prevBass = 0
    prevChord = []
    for i in range(len(chords)):
        c = str_to_pitches(chords[i], prevBass)
        nextChord = [] if i + 1 >= len(chords) else str_to_pitches(chords[i + 1], c[0])
        for n in c:
            if n not in prevChord:
                midi.update_time(time, relative = False)
                midi.note_on(0, n, V)
        time += 8
        for n in c:
            if n not in nextChord:
                midi.update_time(time, relative = False)
                midi.note_off(0, n, V)
        prevBass = c[0]
        prevChord = c
    midi.update_time(0)
    midi.end_of_track()


chords = ['0', '0', '0', '1', '0', '1', '2', '0', 'T', '0', 'E8', '08', 'TT', '0T', '03T', '468E', '068', '84T', '04T', '04T', '04T', '04T', '5', '0', 'T29', '029', '02', '02', '02', '935', '035', '037', '037', '037', '037', '037', '74', '04', '04', '04', '04', '04', '04', 'T', '0', 'E369', 'T58E', '058E', '2269', '0269']
write_file('midi_files/test.mid', chords)
