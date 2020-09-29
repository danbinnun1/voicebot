from pydub import AudioSegment
import Data
import Member
from SoundException import SoundException
from SoundError import SoundError
import Tone
import Vowel
import os

_space = ' '
# space time in milliseconds
_spaceTime = 300


def generateSentence(sentenceString, speaker, outputPath):
    if not speaker in Member.members.keys():
        raise SoundException(
            SoundError.USERNAME_DOES_NOT_EXIST)
    if not Tone.finishedRegisteration(Member.members[speaker]):
        raise SoundException(
            SoundError.USER_NOT_FINISHED_REGISTERETION)
    if len(sentenceString) % 2 == 1:
        raise SoundException(
            SoundError.INVALID_SENTENCE)
    i = 0
    sentenceAudio = AudioSegment.silent(0)
    while i < len(sentenceString):
        syllable = sentenceString[i:i+2]
        tone = syllable[0]
        vowel = syllable[1]
        if tone == _space and vowel == _space:
            sentenceAudio = sentenceAudio+AudioSegment.silent(300)
        elif not tone in Tone.tones or not vowel in Vowel.vowels:
            raise SoundException(
                SoundError.INVALID_SENTENCE)
        else:
            sentenceAudio = sentenceAudio + \
                AudioSegment.from_mp3(os.path.join(
                    Data.recordingsFolderPath, speaker, tone, vowel) + '.mp3')
        i += 2
    sentenceAudio.export(
        outputPath,
        bitrate="192k",
        format="mp3"
    )
