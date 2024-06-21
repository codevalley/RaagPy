class Note:
    ABS_SCALE = 12
    NOTES = 'SRGMPDN'  # Valid notes in order for Indian music notation
    BASE_INDICES = [0, 2, 4, 5, 7, 9, 11]  # Starting indices for each note in a chromatic scale
    INDEX_MAP = {
        0: (0, 0),  # S natural
        1: (1, -1), # R flat
        2: (1, 0),  # R natural
        3: (2, -1), # G flat
        4: (2, 0),  # G natural
        5: (3, 0),  # M natural
        6: (3, 1),  # M sharp
        7: (4, 0),  # P natural
        8: (5, -1), # D flat
        9: (5, 0),  # D natural
        10: (6, -1),# N flat
        11: (6, 0)  # N natural
    }
    def __init__(self, note, octave=0, semitone=0):
        if not isinstance(note, str) or note.upper() not in Note.NOTES:
            raise ValueError("Invalid note, must be one of S, R, G, M, P, D, N")
        self.base_note = Note.NOTES.index(note.upper())  # Convert note letter to an index
        self.octave = octave
        self.semitone = semitone  # -1 = flat, 0 = natural, 1 = sharp
        self.index = self.toNumber()

    def toNumber(self):
        note_index = Note.BASE_INDICES[self.base_note] + self.semitone
        total_index = note_index + (self.octave * 12)
        return total_index
    
    def update(self, note=None, octave=None, semitone=None):
        if note is not None:
            if not isinstance(note, str) or note.upper() not in Note.NOTES:
                raise ValueError("Invalid note, must be one of S, R, G, M, P, D, N")
            self.base_note = note.upper()
        if octave is not None:
            self.octave = octave
        if semitone is not None:
            self.semitone = semitone
        self.index = self.toNumber()  # Update index

    @staticmethod
    def fromNumber(index):
        octave, position_in_octave = divmod(index,Note.ABS_SCALE)
        base_note, semitone = Note.INDEX_MAP[position_in_octave]
        return Note(Note.NOTES[base_note], octave, semitone)

    def __str__(self):
        #semitone_symbol = {1: '#', 0: '', -1: 'b'}
        #return f"{self.base_note}{semitone_symbol[self.semitone]}{' ' + str(self.octave) if self.octave != 0 else ''}"
        # Convert the integer back to the note character for display
        note_char = Note.NOTES[self.base_note]
        if(self.semitone != 0):
            note_char = note_char + "_"
        if self.octave == 0:
            return note_char
        elif self.octave == -1:
            return note_char.lower()
        elif self.octave == 1:
            return note_char + "'"

    
    def transpose(self,steps):
        new_index = self.index + steps
        return Note.fromNumber(new_index)
    
    def compare_base(self, other):
        if isinstance(other, Note):
            return self.base_note == other.base_note
        return False

    def compare_note(self, other):
        if isinstance(other, Note):
            return (self.base_note == other.base_note) and (self.semitone == other.semitone)
        return False

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.index == other.index
        return False
    
    def __lt__(self, other):
        if isinstance(other, Note):
            return self.index < other.index  # Use the pre-computed index for comparison
        return False

    def __hash__(self):
        return hash((self.index,))  # Hash based on the index
    

class NoteContainer:
    def __init__(self):
        self.notes = {}

    def add(self, note):
        self.notes[note.index] = note

    def __contains__(self, item):
        if isinstance(item, Note):
            return item.index in self.notes
        return item in self.notes

    def __str__(self):
        return ', '.join(str(note) for note in self.notes.values())

