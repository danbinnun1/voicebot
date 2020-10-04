import sys
sys.path.append('.')
from src.BL.SoundError import SoundError
from src.BL.SoundException import SoundException
from pydub import AudioSegment
from src.BL.BLconfig import tones, vowels
from src.DAL.DALRecording import getVowelRecording


def generateSentence(name, sentence):
    space = ' '
    words=sentence.split(space)
    for word in words:
        syllables=_splitBySyllables(word)

    

def _splitBySyllables(sentence):
    syllables = []
    if len(sentence) == 0:
        return []
    if len(sentence) == 1:
        if sentence in tones:
            return [(sentence, '.')]
        if sentence in vowels:
            return [('.', sentence)]
        raise SoundException(SoundError.INVALID_SENTENCE)
    if len(sentence) == 2:
        if sentence in tones:
            return [(sentence, '.')]
        if sentence[0] in tones and sentence[1] in vowels:
            return [(sentence[0], sentence[1])]
        return _splitBySyllables(sentence[0]) + _splitBySyllables(sentence[1])
    if sentence[0] in vowels:
        return [('.', sentence[0])]+_splitBySyllables(sentence[1:])
    if sentence[0:2] in tones:
        if sentence[2] in vowels:
            return [(sentence[0:2], sentence[2])]+_splitBySyllables(sentence[3:])
        return [(sentence[0:2],'.')]+_splitBySyllables(sentence[2:])
    if sentence[0] in tones:
        if sentence[1] in vowels:
            return [(sentence[0], sentence[1])]+_splitBySyllables(sentence[2:])
        return [(sentence[0],'.')]+_splitBySyllables(sentence[1:])
    raise SoundException(SoundError.INVALID_SENTENCE)

print(_splitBySyllables(input()))