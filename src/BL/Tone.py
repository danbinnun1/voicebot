from src.BL.SoundError import SoundError
from src.BL.SoundException import SoundException
from src.BL.BLconfig import BLconfig

tones=BLconfig.getTones()

class Tone:
    def __init__(self, tone):
        found = False
        for i, letter in enumerate(tones):
            if letter == tone:
                self.letter = tone
                self.index = i
                found = True
                break
        if not found:
            raise SoundException(SoundError.TONE_DOES_NOT_EXIST)

    def finished(self):
        return tones[-1] == self.letter

    def __gt__(self, other):
        return self.index > other.index

    def __ge__(self, other):
        return self.index >= other.index

    def __eq__(self, other):
        return self.index == other.index

    def __lt__(self, other):
        return self.index < other.index

    def __le__(self, other):
        return self.index <= other.index

    def next(self):
        if self.finished():
            raise SoundException(SoundError.TONE_DOES_NOT_EXIST)
        return Tone(tones[self.index+1])

    @staticmethod
    def first():
        return Tone(tones[0])
