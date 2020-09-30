import sqlite3
from SoundError import SoundError
from SoundException import SoundException
from SoundParser import splitSound
from Tone import Tone
import Data
import os
from pydub import AudioSegment


class Member:
    def __init__(self, name, password, tone):
        self.name = name
        self.__password = password
        self.tone = tone

    def save(self):
        conn = sqlite3.connect(Data.progressFilePath)
        c = conn.cursor()
        searchParameters = (self.name,)
        searchResult = c.execute('''
        SELECT * FROM members WHERE name=?
        ''', searchParameters).fetchone()
        if searchResult != None:
            raise SoundException(SoundError.USERNAME_TAKEN)
        values = (self.name, self.__password, self.tone.letter,)
        c.execute('''
        INSERT INTO members (name, password, progress) VALUES (?,?,?)
        ''', values)
        conn.commit()
        conn.close()
        os.mkdir(os.path.join(Data.recordingsFolderPath,self.name))

    def uploadSound(self, filepath, tone):
        # this is a repair of existing tone
        if tone < self.tone:
            SoundParser.splitSound(filepath, os.path.join(
                Data.recordingsFolderPath, self.name, tone))
        elif tone == self.tone:
            SoundParser.splitSound(filepath, os.path.join(
                Data.recordingsFolderPath, self.name, tone))
            self.tone = self.tone.next()
            conn = sqlite3.connect(Data.progressFilePath)
            c = conn.cursor()
            values = (self.tone.letter, self.name, self.__password)
            c.execute('''
            UPDATE members SET tone=? WHERE name=? AND password=?
            ''', values)
            conn.commit()
            conn.close()
        else:
            raise SoundException(
                SoundError.SENT_RECORDING_AFTER_PROGRESS)

    def generateSentence(self, sentence, outputpath):
        space=' '
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


def getMemberBynameAndPassword(name, password):
    conn = sqlite3.connect(Data.progressFilePath)
    c = conn.cursor()
    values = (name,)
    c.execute('''
    SELECT * FROM members WHERE name=? AND password = ?
    ''', values)
    result = c.fetchone()
    if result == None:
        raise SoundException(SoundError.WRONG_USERNAME_OR_PASSWORD)
    member = Member(result[0], result[1], result[2])
    conn.close()
    return member
