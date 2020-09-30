import os
import shutil
import sys
sys.path.append('..')
from src.DAL import DALMember, Data

datapath='./data'
def test_insertMember():
    if os.path.isdir(datapath):
        shutil.rmtree(datapath)
    Data.initializeData()
    DALMember.insertMember('dan','123','a')
    assert(DALMember.memberExists('dan', '123'))
    assert(DALMember.getMemberProgress('dan')=='a')
    DALMember.insertMember('1','2','3')
    assert(DALMember.getAllMembers()==[('dan','a','123'),('1','3','2')])
