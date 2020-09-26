import os
import zipfile

_dataFolderPath='../data'
_recordingsFolderPath=_dataFolderPath+'/recordings'
_temporalRecordingsFolderPath=_dataFolderPath+'/temporalRecordings'
_progressFilePath=_dataFolderPath+'/progress.txt'

def _initializeData():
    if not os.path.isdir(_dataFolderPath):
        os.mkdir(_dataFolderPath)
        os.mkdir(_recordingsFolderPath)
        os.mkdir(_temporalRecordingsFolderPath)
        progressFile=open(_progressFilePath, 'x')
        progressFile.close()


def temporalFilePath(filename):
    return _temporalRecordingsFolderPath+'/'+filename

def recordingPath(username, tone, vowel):
    return _recordingsFolderPath+'/'+username+'/'+tone+'/'+vowel

def toneRecordingPath(username, tone):
    return _recordingsFolderPath+'/'+username+'/'+tone
    
def zipUserTone(username, tone, filename):
    with zipfile.ZipFile(temporalFilePath(filename), mode='w') as zipf:
        len_dir_path = len(toneRecordingPath(username,tone))
        for root, _, files in os.walk(toneRecordingPath(username,tone)):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])


_initializeData()