import validate
import os
import shutil

datapath='./data'
def test_insertMember():
    if os.path.isdir(datapath):
        shutil.rmtree(datapath)
