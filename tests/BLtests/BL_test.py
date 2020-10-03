import sys
sys.path.append('.')
from src.BL.Member import Member
from pydub import AudioSegment
import os
import shutil
from src.BL import Data
from src.BL.Tone import Tone

def test_bl():
    if os.path.isdir('./data'):
        shutil.rmtree('./data')
    Data.initializeData()
    member=Member.initializeMember('dan')
    member.save('123')
    member.uploadSound(AudioSegment.from_file('./tests/BLtests/testsData/Recording (5).m4a'), Tone('a'))
    member.zipTone(Tone('a'), 'a.zip')
    os.remove('a.zip')