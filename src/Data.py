import os

_dataFolderPath='../data'
_recordingsFolderPath=_dataFolderPath+'/recordings'
_temporalRecordingsFolderPath=_dataFolderPath+'/temporalRecordings'
_progressFilePath=_dataFolderPath+'/progress.txt'

def initializeData():
    if not os.path.isdir(_dataFolderPath):
        os.mkdir(_dataFolderPath)
        os.mkdir(_recordingsFolderPath)
        os.mkdir(_temporalRecordingsFolderPath)
        progressFile=open(_progressFilePath, 'x')
        progressFile.close()


def temporalFilePath(filename):
    return _temporalRecordingsFolderPath+'/'+filename

def recordingPath(username, tone, vowel):
    return recordingPath+'/'+username+'/'+tone+'/'+vowel

def toneRecordingPath(username, tone):
    return recordingPath+'/'+username+'/'+tone
    

initializeData()