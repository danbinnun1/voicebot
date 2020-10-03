import os
import shutil
import sys
sys.path.append('.')
from src.DAL import DALMember, Data, DALRecording
from pydub import AudioSegment

datapath='./data'
def test_insertMember():
    if os.path.isdir(datapath):
        shutil.rmtree(datapath)
    Data.initializeData()
    DALMember.insertMember('dan','123','a')
    assert(DALMember.memberExists('dan', '123'))
    assert(not DALMember.memberExists('dan', '12'))
    assert(not DALMember.memberExists('da', '123'))

    assert(DALMember.usernameExists('dan'))
    assert(not DALMember.usernameExists('da'))

    assert(DALMember.getMemberProgress('dan')=='a')
    DALMember.insertMember('1','2','3')
    assert(DALMember.getAllMembers()==[('dan','a','123'),('1','3','2')])

    DALMember.updateUserProgress('b','dan')
    assert(DALMember.getMemberProgress('dan')=='b')

def test_recordings():
    if os.path.isdir(datapath):
        shutil.rmtree(datapath)
    Data.initializeData()
    DALMember.insertMember('dan','123','a')
    vowels=['a','e','i','o','u','.']
    for vowel in vowels:
        DALRecording.uploadVowelRecording(AudioSegment.from_mp3(os.path.join('./tests/DALtests/testsData/input/a', vowel+'.mp3')),'dan','a',vowel)

    for vowel in vowels:
        assert(AudioSegment.from_file(os.path.join('./tests/DALtests/testsData/expectedresult/a', vowel+'.mp3')).raw_data==DALRecording.getVowelRecording('dan','a',vowel).raw_data)