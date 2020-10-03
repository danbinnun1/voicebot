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
from src.BL.SentenceGenerator import generateSentence

class Member:
    def __init__(self, name, tone):
        self.__name = name
        self.__tone = tone

    def save(self, password):
        if DALMember.usernameExists(self.__name):
            raise SoundException(SoundError.USERNAME_TAKEN)
        DALMember.insertMember(self.__name, password, self.__tone.letter)

    def uploadSound(self, recording, tone):
        # this is a repair of existing tone
        if tone < self.__tone:
            toneVowels = splitSound(recording)
            for i, vowelRecording in enumerate(toneVowels):
                DALRecording.uploadVowelRecording(vowelRecording,self.__name, tone.letter, vowels[i])
        elif tone == self.__tone:
            toneVowels = splitSound(recording)
            for i, vowelRecording in enumerate(toneVowels):
                DALRecording.uploadVowelRecording(vowelRecording,self.__name, tone.letter, vowels[i])
            DALMember.updateUserProgress(self.__tone.next(), self.__name)
        else:
            raise SoundException(
                SoundError.SENT_RECORDING_AFTER_PROGRESS)

    def generateSentence(self, sentence):
        if not self.__tone.finished():
            raise SoundException(
                SoundError.USER_NOT_FINISHED_REGISTERETION)
        return generateSentence(self.__name, sentence)
    def zipTone(self, tone, outputpath):
        DALMember.zipUserTone(self.__name, self.__tone.letter, outputpath)

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

    @staticmethod
    def initializeMember(name):
        return Member(name, Tone.first())