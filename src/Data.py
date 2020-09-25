import os

dataFolderPath='../data'
recordingsFolderPath=dataFolderPath+'/recordings'
temporalRecordingsFolderPath=dataFolderPath+'/temporalRecordings'
progressFilePath=dataFolderPath+'/progress.txt'

def initializeData():
    if not os.path.isdir(dataFolderPath):
        os.mkdir(dataFolderPath)
        os.mkdir(recordingsFolderPath)
        os.mkdir(temporalRecordingsFolderPath)
        progressFile=open(progressFilePath, 'x')
        progressFile.close()


initializeData()