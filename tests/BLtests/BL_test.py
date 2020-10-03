import sys
sys.path.append('.')
from src.BL.Member import Member
from pydub import AudioSegment
import os
import shutil
from src.BL import Data, SentenceGenerator
from src.BL.SoundError import SoundError
from src.BL.SoundException import SoundException
from src.BL.Tone import Tone
import filecmp

def test_bl():
    if os.path.isdir('./data'):
        shutil.rmtree('./data')
    Data.initializeData()
    tones=open('settings/tones.txt','r').read()
    with open('settings/tones.txt','w') as tonesFile:
        tonesFile.write('a,b,#')
    tonesFile.close()

    member1=Member.initializeMember('dan')
    member1.save('123')
    recording=AudioSegment.from_file('./tests/BLtests/testsData/Recording (5).m4a')
    member1.uploadSound(recording, Tone('a'))
    member1.zipTone(Tone('a'), 'a.zip')
    os.remove('a.zip')
    member1.uploadSound(recording,Tone('b'))
    heni=Member.initializeMember('heni')
    heni.save('12')
    exceptionThrown=False
    try:
        heni.uploadSound(recording, Tone('b'))
    except SoundException as e:
        if (e.errorCode==SoundError.SENT_RECORDING_AFTER_PROGRESS):
            exceptionThrown=True
    assert(exceptionThrown)
    exceptionThrown=False
    heni.uploadSound(recording, Tone('a'))
    heni.uploadSound(recording, Tone('a'))
    heni.uploadSound(recording, Tone('b'))
    heni.uploadSound(recording, Tone('a'))
    heni.generateSentence('aa')
    try:
        heni.uploadSound(recording, Tone('c'))
    except SoundException as e:
        if e.errorCode==SoundError.TONE_DOES_NOT_EXIST:
            exceptionThrown=True
    assert(exceptionThrown)
    exceptionThrown=False
    hapanter=Member.getMemberBynameAndPassword('heni','12')
    hapanter.generateSentence('aa')
    kush=Member.initializeMember('kush')
    kush.save('63')
    kush.uploadSound(recording,Tone('a'))
    kush2=Member.getMemberBynameAndPassword('kush','63')
    try:
        kush2.generateSentence('aa')
    except SoundException as e:
        if e.errorCode==SoundError.USER_NOT_FINISHED_REGISTERETION:
            exceptionThrown=True
    assert(exceptionThrown)
    exceptionThrown=False
    kush2.uploadSound(recording,Tone('b'))
    kush=Member.getMemberByusername('kush')
    kush.generateSentence('aa')
    try:
        Member.getMemberBynameAndPassword('kush','123')
    except SoundException as e:
        if e.errorCode==SoundError.WRONG_USERNAME_OR_PASSWORD:
            exceptionThrown=True
    assert(exceptionThrown)
    exceptionThrown=False
    try:
        Member.getMemberByusername('123')
    except SoundException as e:
        if e.errorCode==SoundError.USERNAME_DOES_NOT_EXIST:
            exceptionThrown=True
    assert(exceptionThrown)
    with open('settings/tones.txt','w') as tonesFile:
        tonesFile.write(tones)
    tonesFile.close()
