import os

_dataFolderPath = '/home/danbinnun1/voicebot/data'
recordingsFolderPath = os.path.join(_dataFolderPath, 'recordings')
temporalRecordingsFolderPath = os.path.join(
    _dataFolderPath, 'temporalRecordings')
progressFilePath = os.path.join(_dataFolderPath, 'progress.db')
