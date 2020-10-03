from src.BL.SoundError import SoundError
from src.BL.SoundException import SoundException
from src.BL.SoundParser import splitSound
from src.BL.Tone import Tone
from src.BL.BLconfig import tones
import os
from pydub import AudioSegment
import src.DAL.DALMember as DALMember
import src.DAL.DALRecording as DALRecording
from src.BL.BLconfig import vowels

class Member:
    def __init__(self, name, tone):
        self.name = name
        self.tone = tone

    def save(self, password):
        if DALMember.usernameExists(self.name):
            raise SoundException(SoundError.USERNAME_TAKEN)
        DALMember.insertMember(self.name, password, self.tone)

    def uploadSound(self, recording, tone):
        # this is a repair of existing tone
        if tone < self.tone:
            toneVowels = splitSound(recording)
            for i, vowelRecording in enumerate(toneVowels):
                DALRecording.uploadVowelRecording(vowelRecording,self.name, tone.letter, vowels[i])
        elif tone == self.tone:
            toneVowels = splitSound(recording)
            for i, vowelRecording in enumerate(toneVowels):
                DALRecording.uploadVowelRecording(vowelRecording,self.name, tone.letter, vowels[i])
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
    def zipTone(self, tone, outputpath):
        DALMember.zipUserTone(self.name, tone, outputpath)

    @staticmethod
    def getMemberBynameAndPassword(username, password):
        if not DALMember.memberExists(username, password):
            raise SoundException(SoundError.WRONG_USERNAME_OR_PASSWORD)
        return Member(username, Tone(DALMember.getMemberProgress(username)))

    @staticmethod
    def getMemberByusername(username):
        if not DALMember.usernameExists(username):
            raise SoundException(SoundError.USERNAME_DOES_NOT_EXIST)
        return Member(username, Tone(DALMember.getMemberProgress(username)))

    @staticmethod
    def getAllMembers():
        rows=DALMember.getAllMembers()
        members = {}
        for row in rows:
            members[row[0]] = row[1]
        return members