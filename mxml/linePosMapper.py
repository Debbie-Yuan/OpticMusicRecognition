GClefMappingXML = {
    0: 'f3',
    1: 'g3',
    2: 'a3',
    3: 'b3',
    4: 'c4',
    5: 'd4',
    6: 'e4',
    7: 'f4',
    8: 'g4',
    9: 'a4',
    10: 'b4',
    11: 'c5',
    12: 'd5',
    13: 'e5',
    14: 'f5',
    15: 'g5',
    16: 'a5',
    17: 'b5',
    18: 'c6',
    19: 'd6',
    20: 'e6'
}

FClefMapping = {
    0: 'A1',
    1: 'B1',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'A',
    8: 'B',
    9: 'c',
    10: 'd',
    11: 'e',
    12: 'f',
    13: 'g',
    14: 'a',
    15: 'b',
    16: 'c1',
    17: 'd1',
    18: 'e1',
    19: 'f1',
    20: 'g1'
}

FClefMappingXML = {
    0: 'a1',
    1: 'b1',
    2: 'C2',
    3: 'D2',
    4: 'E2',
    5: 'F2',
    6: 'G2',
    7: 'A2',
    8: 'B2',
    9: 'c3',
    10: 'd3',
    11: 'e3',
    12: 'f3',
    13: 'g3',
    14: 'a3',
    15: 'b3',
    16: 'c4',
    17: 'd4',
    18: 'e4',
    19: 'f4',
    20: 'g4'
}

DurationMapping = {
    21: 4,
    22: 2,
    23: 1,
    24: 0.5,
    25: 0.25,
    26: 0.125,
    27: 0.0625
}

AttrMapping = {
    28: 'stop',
    29: 'dot',
    30: 'down',
    31: 'up'
}


class NoteConvertor:

    def __init__(self, clef='g', clap=(4, 4)):
        self.__clef = clef
        self.c_a = clap[0]
        self.c_b = clap[1]

    def __getitem__(self, item):
        assert 0 <= item <= 31
        if 0 <= item < 21:
            if self.__clef == 'g':
                return GClefMappingXML.get(item)
            else:
                return FClefMappingXML.get(item)
        elif 21 <= item <= 27:
            return DurationMapping.get(item)
        else:
            return AttrMapping.get(item)

    def __len__(self):
        return 32

    def __call__(self, note_vector, *args, **kwargs):
        if len(note_vector) == 0:
            return None
        speed = set(note_vector) & set(range(21, 28, 1))
        if len(speed) <= 0:
            if note_vector[0] == 28:
                return {
                    'clear': False,
                    'rest': True,
                    'speed': -1,
                    'dot': False
                }
            else:
                return {'clear': False}
        notes = set(note_vector) & set(range(0, 21, 1))
        if len(notes) <= 0:
            return {'clear': False}

        speed = self[tuple(speed)[0]]
        dot = True if 29 in note_vector else False

        if 28 in note_vector:
            res = {
                'clear': True,
                'rest': True,
                'speed': speed,
                'dot': dot,
            }
        else:
            res = {
                'clear': True,
                'rest': False,
                'notes': [self[i] for i in list(notes)],
                'speed': speed,
                'dot': dot,
                'up': True if 31 in note_vector else False,
                'down': True if 30 in note_vector else False
            }
        return res

    def set_g_clef(self):
        self.__clef = 'g'

    def set_f_clef(self):
        self.__clef = 'f'

    @staticmethod
    def sharpen_note(note_str: str):
        if len(note_str) == 2:
            return f"{note_str[0]}#{note_str[1]}"
        else:
            return f"#{note_str}"

    @staticmethod
    def lower_note(note_str: str):
        if len(note_str) == 2:
            return f"{note_str[0]}b{note_str[1]}"
        else:
            return f"b{note_str}"
