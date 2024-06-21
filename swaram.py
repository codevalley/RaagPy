class Note:
    ABS_SCALE = 12 #chromatic scale has 12 notes
    SYMBOL = " " #A symbol which is not a note, but can be used as a placeholder
    SYMBOL_INDEX = 999999  #Just a really large number, for a non-note placeholder
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
        #initialize these variables
        self.symbol = None
        self.base_note = 0
        #Could be a note or a placeholder
        if isinstance(note,str):
            if note.upper() in Note.NOTES:
                self.base_note = Note.NOTES.index(note.upper())  # Convert note letter to an index
            else:
                self.symbol = note
        elif isinstance(note, int):
            self.base_note = note % Note.ABS_SCALE
        else:
            raise ValueError("Must be a string or a number")
        
        self.octave = octave
        self.semitone = semitone  # -1 = flat, 0 = natural, 1 = sharp
        self.index = self.toNumber()


    def update(self, note=None, octave=None, semitone=None):
        if note is not None:
            if isinstance(note, str):
                if note.upper() in Note.NOTES:
                    self.base_note = Note.NOTES.index(note.upper())
                    self.symbol = None  # Clear the symbol since it's a valid note
                else:
                    self.symbol = note  # Assign non-note symbols
            elif isinstance(note, int):
                self.base_note = note % Note.ABS_SCALE
                self.symbol = None  # Ensure no symbol is set when using numerical notes
            else:
                raise ValueError("Note must be a string or an integer")

        if octave is not None:
            self.octave = octave
        if semitone is not None:
            self.semitone = semitone

        self.index = self.toNumber()  # Recalculate index after updates

    
    def transpose(self,steps):
        if self.symbol != None:
            return self
        new_index = self.index + steps
        return Note.fromNumber(new_index)
    
    def compare_base(self, other):
        if isinstance(other, Note):
            if self.symbol != None and other.symbol != None: 
                return True  # Assume all symbols are equivalent
            return self.base_note == other.base_note
        return False

    def compare_note(self, other):
        if isinstance(other, Note):
            if self.symbol is not None and other.symbol is not None:
                return True  # Assume all symbols are equivalent
            return (self.base_note == other.base_note) and (self.semitone == other.semitone)
        return False

    def toNumber(self):
        if(self.symbol != None):
            return self.SYMBOL_INDEX
        
        note_index = Note.BASE_INDICES[self.base_note] + self.semitone
        total_index = note_index + (self.octave * self.ABS_SCALE)
        return total_index
    
    @staticmethod
    def fromNumber(index):
        if index == Note.SYMBOL_INDEX:
            return Note(Note.SYMBOL)
        octave, position_in_octave = divmod(index,Note.ABS_SCALE)
        base_note, semitone = Note.INDEX_MAP[position_in_octave]
        return Note(Note.NOTES[base_note], octave, semitone)
    

    #overloaded internal methods

    def __str__(self):
        if self.symbol != None:
            return self.symbol

        note_char = Note.NOTES[self.base_note]
        if(self.semitone != 0):
            note_char = note_char + "_"
        if self.octave == 0:
            return note_char
        elif self.octave == -1:
            return note_char.lower()
        elif self.octave == 1:
            return note_char + "'"
        
    def __eq__(self, other):
        if isinstance(other, Note):
            if self.symbol is not None and other.symbol == self.symbol:
                return True  # Check for symbol equality
            return self.index == other.index
        return False
    
    def __lt__(self, other):
        if isinstance(other, Note):
            return self.index < other.index  # Use the pre-computed index for comparison
        return NotImplemented

    def __hash__(self):
        return hash((self.index,))   # Hash based on the index
    

class NoteContainer:
    def __init__(self):
        self.notes = OrderedDict()

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

    def normalize(self):
        """Normalizes all notes to octave 0 and returns a new NoteContainer with these normalized notes."""
        normalized_container = NoteContainer()
        for note in self.notes.values():
            normalized_note = Note(note.base_note, 0, note.semitone)  # Normalize to octave 0
            normalized_container.add(normalized_note)
        return normalized_container
    
    def __iter__(self):
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
    def getLast(self):
        # Return the last item without removing it, if the list is not empty
        return self.notes[-1] if self.notes else None