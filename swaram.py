class Note:
    NOTES = 'SRGMPDN'  # Valid notes in order for Indian music notation

    def __init__(self, note, octave=0, semitone=0):
        if note.upper() not in Note.NOTES:
            raise ValueError("Invalid note, must be one of S, R, G, M, P, D, N")
        self.base_note = Note.NOTE_ORDER.index(note.upper())  # Convert note letter to an index
        self.octave = octave
        self.semitone = semitone  # -1 = flat, 0 = natural, 1 = sharp

    def __str__(self):
        #semitone_symbol = {1: '#', 0: '', -1: 'b'}
        #return f"{self.base_note}{semitone_symbol[self.semitone]}{' ' + str(self.octave) if self.octave != 0 else ''}"
        # Convert the integer back to the note character for display
        note_char = Note.NOTE_ORDER[self.base_note]
        if self.octave == 0:
            return note_char
        elif self.octave == -1:
            return note_char.lower()
        elif self.octave == 1:
            return note_char + "'"
    
    def transpose(self,steps):
        # Calculate the new note index and handle octave wrapping
        new_note_index = (self.base_note + steps) % len(Note.NOTE_ORDER)
        new_octave = self.octave + ((self.base_note + steps) // len(Note.NOTE_ORDER))
        # Handle negative steps for correct octave calculation
        if steps < 0 and (self.base_note + steps) < 0:
            new_octave -= 1
        return Note(Note.NOTE_ORDER[new_note_index], new_octave, 0)
    
    def compare_base(self, other):
        return self.base_note == other.base_note

    def compare_note(self, other):
        return (self.base_note == other.base_note) and (self.semitone == other.semitone)

    def __eq__(self, other):
        # Default equality for all purposes
        return (self.base_note == other.base_note) and (self.octave == other.octave) and (self.semitone == other.semitone)
    def __lt__(self, other):
        # Define order for sorting based on the Indian classical music order
        order = 'SRGMPDN'
        # Sorting by base note and then by octave
        if self.base_note == other.base_note:
            return self.octave < other.octave
        return order.index(self.base_note) < order.index(other.base_note)

    def __hash__(self):
        # Allows note to be used in sets and as dictionary keys
        return hash((self.base_note, self.octave))

# Example usage
note = Note('N')
transposed_note = note.transpose()
transposed_note2 = transposed_note.transpose()

print("Original Note:", note)  # Output: N
print("Transposed Note 1:", transposed_note)  # Output: N#
print("Transposed Note 2:", transposed_note2)  # Output: S
