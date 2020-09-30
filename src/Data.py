import os
import zipfile
import sqlite3

_dataFolderPath = '../data'
recordingsFolderPath = os.path.join(_dataFolderPath, 'recordings')
temporalRecordingsFolderPath = os.path.join(
    _dataFolderPath, 'temporalRecordings')
progressFilePath = str(os.path.join(_dataFolderPath, 'progress.db'))


def _initializeData():
    if not os.path.isdir(_dataFolderPath):
        os.mkdir(_dataFolderPath)
        os.mkdir(recordingsFolderPath)
        os.mkdir(temporalRecordingsFolderPath)
        conn = sqlite3.connect(progressFilePath)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE members (name text, progress text, password text);
        ''')
        conn.commit()
        conn.close()


def zipUserTone(username, tone, filepath):
    with zipfile.ZipFile(filepath, mode='w') as zipf:
        dir_path = os.path.join(recordingsFolderPath, username, tone)
        len_dir_path = len(dir_path)
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])


_initializeData()
