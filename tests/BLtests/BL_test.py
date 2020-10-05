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
from src.BL.BLconfig import BLconfig
import filecmp

def test_bl():
    if os.path.isdir('./data'):
        shutil.rmtree('./data')
    Data.initializeData()
    
    tonesData=''
    with open('./settings/tones.txt', 'r') as settings:
        tonesData=settings.read()
        settings.close()
    with open('./settings/tones.txt', 'w') as settings:        
        settings.write('_,b,ch,#')
        settings.close()

    tones=BLconfig.getTones()
    vowels=BLconfig.getVowels()

    member1=Member.initializeMember('jhg', 'fff')
    recording_=AudioSegment.from_file('./tests/BLtests/testsData/_.ogg')
    recordingb=AudioSegment.from_file('./tests/BLtests/testsData/b.ogg')
    recordingch=AudioSegment.from_file('./tests/BLtests/testsData/ch.ogg')

    member1.uploadSound(recording_, '_')
    member1.zipTone('_', 'a.zip')
    #assert(filecmp.cmp('a.zip','tests/BLtests/testsData/a.zip'))
    os.remove('a.zip')
    member1.uploadSound(recordingb,'b')
    member1.uploadSound(recording_,'_')
    member1.uploadSound(recordingb,'b')
    
    heni=Member.initializeMember('heni','123')
    exceptionThrown=False
    try:
        heni.uploadSound(recordingb, 'b')
    except SoundException as e:
        if (e.errorCode==SoundError.SENT_RECORDING_AFTER_PROGRESS):
            exceptionThrown=True
    assert(exceptionThrown)
    exceptionThrown=False
    heni.uploadSound(recording_, '_')
    heni.uploadSound(recording_, '_')
    heni.uploadSound(recordingb, 'b')
    heni.uploadSound(recording_, '_')
    heni.uploadSound(recordingch,'ch')
    heni.generateSentence('aa')
    try:
        heni.uploadSound(recordingch, 'c')
    except SoundException as e:
        if e.errorCode==SoundError.TONE_DOES_NOT_EXIST:
            exceptionThrown=True
    assert(exceptionThrown)
    exceptionThrown=False
    hapanter=Member.getMemberBynameAndPassword('heni','123')
    hapanter.generateSentence('aa')
    kush=Member.initializeMember('kush','63')
    kush.uploadSound(recording_,'_')
    kush2=Member.getMemberBynameAndPassword('kush','63')
    try:
        kush2.generateSentence('aa')
    except SoundException as e:
        if e.errorCode==SoundError.USER_NOT_FINISHED_REGISTERETION:
            exceptionThrown=True
    assert(exceptionThrown)
    exceptionThrown=False
    kush2.uploadSound(recordingb,'b')
    kush=Member.getMemberByusername('kush')
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
    
