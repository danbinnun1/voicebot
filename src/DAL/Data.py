import DAL.DALconfig as config
import os
import sqlite3

def initializeData():
    if not os.path.isdir(config.dataFolderPath):
        os.mkdir(config.dataFolderPath)
        os.mkdir(config.recordingsFolderPath)
        conn = sqlite3.connect(config.progressFilePath)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE members (name text PRIMARY KEY, progress text, password text);
        ''')
        conn.commit()
        conn.close()