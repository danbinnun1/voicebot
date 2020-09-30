from SoundError import SoundError
from SoundException import SoundException
from SoundParser import splitSound
from Tone import Tone
from BL.BLconfig import tones
import os
from pydub import AudioSegment
import DAL.DALMember as DALMember
import DAL.DALRecording as DALRecording
from Vowel import vowels

class Member:
    def __init__(self, name, password, tone):
        self.name = name
        self.__password = password
        self.tone = tone

    def save(self):
        if not DALMember.usernameAvailable(self.name):
            raise SoundException(SoundError.USERNAME_TAKEN)
        DALMember.insertMember(self.name, self.__password, self.tone)

    def uploadSound(self, recording, tone):
        # this is a repair of existing tone
        if tone < self.tone:
            toneVowels = splitSound(recording)
            for i, vowelRecording in enumerate(toneVowels):
                DALRecording.uploadVowelRecording(vowelRecording,self.name, tone, vowels[i])
        elif tone == self.tone:
            toneVowels = splitSound(recording)
            DALMember.updateUserProgress(self.tone.next(), self.name)
        else:
            raise SoundException(
                SoundError.SENT_RECORDING_AFTER_PROGRESS)

    def generateSentence(self, sentence):
        space = ' '
        if not self.tone.finished():
            raise SoundException(
                SoundError.USER_NOT_FINISHED_REGISTERETION)
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
                sentenceAudio += DALRecording.getVowelRecording(self.name, tone, vowel)
            i += 2
        return sentenceAudio


def getMemberBynameAndPassword(username, password):
    if not DALMember.memberExists(username, password):
        raise SoundException(SoundError.WRONG_USERNAME_OR_PASSWORD)
    return Member(username, password, DALMember.getMemberProgress(username))
