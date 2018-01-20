

# from Music for Geeks and Nerds (mingus has all of this)
def mod12(n): return n % 12


def note_name(number):
    return note_name.NOTES[mod12(number)]


note_name.NOTES = "C C# D D# E F F# G G# A A# B".split()


def accidentals(note_string):
    acc = len(note_string[1:])
    if '#' in note_string:
        return acc
    elif 'b' in note_string:
        return -acc
    else:
        return 0


def name_to_number(note_string):
    name = note_string[0:1].upper()
    number = name_to_number.NOTES.index(name)
    acc = accidentals(note_string)
    return mod12(number + acc)


name_to_number.NOTES = "C . D . E F . G . A . B".split()


if __name__ == '__main__':
    import argparse
    import random
    # from mingus.containers.bar import Bar
    from mingus.containers.track import Track

    notes = [0]
    for t in range(30):
        note = notes[-1]
        notes.append(note + random.randint(0, 12))

    t = Track()
    notes = map(note_name, notes)
    for n in notes:
        t.add_notes(n)

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='out.mid')
    args = parser.parse_args()

    from mingus.midi import midi_file_out
    midi_file_out.write_Track(args.output, t)
