import os

dataFolderPath='../data'
recordingsFoledrPath=dataFolderPath+'/recordings'
temporalRecordingsFoledrPath=dataFolderPath+'/temporalRecordings'
progressFilePath=dataFolderPath+'/progress.txt'

def initializeData():
    if not os.path.isdir(dataFolderPath):
        os.mkdir(dataFolderPath)
        os.mkdir(recordingsFoledrPath)
        os.mkdir(temporalRecordingsFoledrPath)
        progressFile=open(progressFilePath, 'x')
        progressFile.close()


initializeData()