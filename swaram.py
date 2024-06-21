class Note:
    ABS_SCALE = 12
    SYMBOL = " "
    SYMBOL_INDEX = 999999  # Just a really large number
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

        self.symbol = None
        self.base_note = 0
        if isinstance(note,str):
            if note.upper() in Note.NOTES:
                self.base_note = Note.NOTES.index(note.upper())  # Convert note letter to an index
            else:
                self.symbol = str
        elif isinstance(note, int):
            self.base_note = note % Note.ABS_SCALE
        else:
            raise ValueError("Must be a string or a number")
        
        self.octave = octave
        self.semitone = semitone  # -1 = flat, 0 = natural, 1 = sharp
        self.index = self.toNumber()

    def toNumber(self):
        if(self.symbol != None):
            return self.SYMBOL_INDEX
        
        note_index = Note.BASE_INDICES[self.base_note] + self.semitone
        total_index = note_index + (self.octave * self.ABS_SCALE)
        return total_index
    
    def update(self, note=None, octave=None, semitone=None):
        if note is not None:
            if isinstance(note,str):
                if note.upper() in Note.NOTES:
                    self.base_note = Note.NOTES.index(note.upper())  # Convert note letter to an index
                else:
                    self.symbol = str
            elif isinstance(note, int):
                self.base_note = note % Note.ABS_SCALE
            else:
                raise ValueError("Must be a string or a number")
        if octave is not None:
            self.octave = octave
        if semitone is not None:
            self.semitone = semitone
        self.index = self.toNumber()  # Update index

    @staticmethod
    def fromNumber(index):
        if index == Note.SYMBOL_INDEX:
            return Note(Note.SYMBOL, octave, semitone)
        octave, position_in_octave = divmod(index,Note.ABS_SCALE)
        base_note, semitone = Note.INDEX_MAP[position_in_octave]
        return Note(Note.NOTES[base_note], octave, semitone)

    def __str__(self):
        
        if self.symbol != None:
            return self.SYMBOL

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
        if self.symbol != None:
            return self
        new_index = self.index + steps
        return Note.fromNumber(new_index)
    
    def compare_base(self, other):
        if isinstance(other, Note):
            if self.symbol != None:
                if other.symbol != None: 
                    # Here we are deliberately ignoring what the symbol string is
                    # And matching all symbols as same
                    return True
            return self.base_note == other.base_note
        return False

    def compare_note(self, other):
        if isinstance(other, Note):
            if self.symbol != None:
                if other.symbol != None: 
                    # Here we are deliberately ignoring what the symbol string is
                    # And matching all symbols as same
                    return True
            return (self.base_note == other.base_note) and (self.semitone == other.semitone)
        return False

    def __eq__(self, other):
        if isinstance(other, Note):
            if self.symbol != None:
                if other.symbol == self.SYMBOL: 
                    return True
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
        return ''.join(str(note) for note in self.notes.values())

    def __len__(self):
        return len(self.notes)

    def pop(self):
        if self.notes:
            # Return the last item from the ordered dictionary
            last_key = next(reversed(self.notes))
            return self.notes[last_key]
        return None

    def normalize(self):
        """Normalizes all notes to octave 0 and returns a new NoteContainer with these normalized notes."""
        normalized_container = NoteContainer()
        for note in self.notes.values():
            normalized_note = Note(note.base_note, 0, note.semitone)  # Normalize to octave 0
            normalized_container.add(normalized_note)
        return normalized_container
    
    def fetch(self, position):
        # Check if the position is within bounds
        if position < 0 or position >= len(self.notes):
            raise IndexError("Position out of bounds")
        # Get the item by index in the ordered dictionary
        key = list(self.notes.keys())[position]
        return self.notes[key]
    
    def __iter__(self):
        """Yield each note in the container."""
        for note in self.notes.values():
            yield note

class NoteList:
    def __init__(self):
        self.notes = []  # Use a list to store notes

    def __getitem__(self, index):
        # Allows direct indexing access
        return self.notes[index]
    
    def __iter__(self):
        """Yield each note in the container."""
        return iter(self.notes)

    def __contains__(self, item):
        # Check for note existence in the list
        return any(item == note for note in self.notes)

    def __str__(self):
        return ''.join(str(note) for note in self.notes)

    def __len__(self):
        return len(self.notes)  # Return the number of notes in the list

    def add(self, note):
        self.notes.append(note)  # Append new note to the list

    def pop(self):
        # Pop the last item from the list if not empty
        return self.notes.pop() if self.notes else None

    def normalize(self):
        """Normalizes all notes to octave 0 and returns a new NoteContainer with these normalized notes."""
        normalized_container = NoteList()
        for note in self.notes:
            normalized_note = Note(note.base_note, 0, note.semitone)  # Normalize to octave 0
            normalized_container.add(normalized_note)
        return normalized_container
    
    def fetch(self, position):
        # Return the item by index in the list, raises IndexError if out of bounds
        return self.notes[position]

    def __getitem__(self, index):
        # Allows direct indexing access
        return self.notes[index]
    
    def __iter__(self):
        """Yield each note in the container."""
        return iter(self.notes)