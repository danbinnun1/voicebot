import os
import shutil
import sys
sys.path.append('..')
import src.DAL.DALMember, src.DAL.Data

datapath='./data'
def test_insertMember():
    if os.path.isdir(datapath):
        shutil.rmtree(datapath)
    src.DAL.Data.initializeData()
    src.DAL.DALMember.insertMember('dan','123','a')
    assert(src.DAL.DALMember.memberExists('dan', '123'))
    assert(src.DAL.DALMember.getMemberProgress('dan')=='a')
    src.DAL.DALMember.insertMember('1','2','3')
    assert(src.DAL.DALMember.getAllMembers()==[('dan','a','123'),('1','3','2')])
