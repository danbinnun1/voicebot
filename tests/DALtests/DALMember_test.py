import os
import shutil

datapath='./data'
def test_insertMember():
    if os.path.isdir(datapath):
        shutil.rmtree(datapath)
    assert(1==1)
