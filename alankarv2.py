import argparse
from swaram import Note, NoteContainer, NoteList
import sys

def note_travel(scale, note, increment):
    """Finds the next note in the scale from the given note."""
    new_note = note
    while True:
        # Transpose the note by one semitone
        new_note = new_note.transpose(increment)
        # Normalize to the 0 octave to check if it exists in the scale
        base_note = Note(new_note.base_note, 0, new_note.semitone)
        # Check if the normalized note exists in the scale container
        if base_note in scale:
            return new_note
        
def parse_scale(scale):
    """ Parses the given scale into a NoteContainer, assuming no semitones and octave 0. """
    container = NoteContainer()
    ## Validate notes to be valid characters
    for char in scale:
        if char.upper() not in Note.NOTES:
            raise ValueError("Invalid note, must be one of S, R, G, M, P, D, N")
        note = Note(char.upper(), 0, 0)  # Normalize all to octave 0, semitone 0
        container.add(note)
    return container

def parse_pattern(pattern):
    """ Parses the pattern into a list of Notes, considering octave info. """
    notes = NoteList()
    i = 0
    while i < len(pattern):
        char = pattern[i]
        
        octave = 0
        if char.islower():  # Lowercase indicates lower octave
            char = char.upper()
            octave = -1
        elif i + 1 < len(pattern) and pattern[i + 1] == "'":
            # Check for apostrophe following a note character
            octave = 1
            i += 1  # Move past the apostrophe

        note = Note(char, octave, 0)
        notes.add(note)
        i += 1
    return notes


def generate_alankars(scale, pattern, shortloop):
    """ Generates alankars by shifting each note in the pattern to the next in the scale. """
    alankars = []
    current_pattern = pattern
    alankars.append(current_pattern)
    while True:
        node = NoteList()
        for note in current_pattern:
            node.add(note_travel(scale,note,1))
    
        alankars.append(node)
        current_pattern = node
        if shortloop == True and node[-1].base_note == 0:
            break;
        if shortloop == False and str(node.normalize()) == str(pattern.normalize()):
            break;
    return alankars

def setup_arg_parser():
    parser = argparse.ArgumentParser(description="Generate Alankars for given Raag scale.")
    parser.add_argument("pattern", type=str, help="The seed pattern of the alankar, e.g., 'SGMDN'")
    parser.add_argument("-s", "--scale", type=str, default="SRGMPDN", help="Optional scale input in CAPS for middle octave. Default is 'SRGMPDNS'")
    parser.add_argument("-l", "--shortloop", type=bool, default=True, help="Loop can be short (ending with S), or long (finishing an octave)")
    return parser
    
def main():
    parser = setup_arg_parser()
    args = parser.parse_args()

    scale = args.scale
    pattern = args.pattern
    shortloop = args.shortloop

    scale_container = parse_scale(scale)
    pattern_notes = parse_pattern(pattern)
    
    alankars = generate_alankars(scale_container, pattern_notes, shortloop)
    for alankar in alankars:
        print(''.join(str(note) for note in alankar))
    

if __name__ == "__main__":
    main()
