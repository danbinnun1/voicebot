from src.BL.SoundError import SoundError
from src.BL.SoundException import SoundException
from pydub import AudioSegment
from src.BL.BLconfig import tones, vowels
from src.DAL.DALRecording import getVowelRecording

def generateSentence(name, sentence):
    space = ' '
    if len(sentence) % 2 == 1:
        raise SoundException(
            SoundError.INVALID_SENTENCE)
    i = 0
    sentenceAudio = AudioSegment.silent(0)
    while i < len(sentence):
        syllable = sentence[i:i+2]
        tone = syllable[0]
        vowel = syllable[1]
        if tone == space and vowel == space:
            sentenceAudio = sentenceAudio+AudioSegment.silent(300)
        elif not tone in tones or not vowel in vowels:
            raise SoundException(
                SoundError.INVALID_SENTENCE)
        else:
            sentenceAudio += getVowelRecording(name, tone, vowel)
        i += 2
    return sentenceAudio