import sys
sys.path.append('.')

from src.DAL.DALRecording import getVowelRecording
from src.BL.BLconfig import tones, vowels
from pydub import AudioSegment
from src.BL.SoundException import SoundException
from src.BL.SoundError import SoundError


def generateSentence(name, sentence):
    space = ' '
    words = sentence.split(space)
    audio = AudioSegment.silent(0)
    for word in words:
        syllables = _splitBySyllables(word)
        for syllable in syllables:
            audio += getVowelRecording(name, syllable[0], syllable[1])
        audio += AudioSegment.silent(300)
    return audio


def _splitBySyllables(sentence):
    ALEPH = '_'
    SHVA = '.'
    syllables = []
    if len(sentence) == 0:
        return []
    if len(sentence) == 1:
        if sentence in tones:
            return [(sentence, SHVA)]
        if sentence in vowels:
            return [(ALEPH, sentence)]
        raise SoundException(SoundError.INVALID_SENTENCE)
    if len(sentence) == 2:
        if sentence in tones:
            return [(sentence, SHVA)]
        if sentence[0] in tones and sentence[1] in vowels:
            return [(sentence[0], sentence[1])]
        return _splitBySyllables(sentence[0]) + _splitBySyllables(sentence[1])
    if sentence[0] in vowels:
        return [(ALEPH, sentence[0])]+_splitBySyllables(sentence[1:])
    if sentence[0:2] in tones:
        if sentence[2] in vowels:
            return [(sentence[0:2], sentence[2])]+_splitBySyllables(sentence[3:])
        return [(sentence[0:2], SHVA)]+_splitBySyllables(sentence[2:])
    if sentence[0] in tones:
        if sentence[1] in vowels:
            return [(sentence[0], sentence[1])]+_splitBySyllables(sentence[2:])
        return [(sentence[0], SHVA)]+_splitBySyllables(sentence[1:])
    raise SoundException(SoundError.INVALID_SENTENCE)