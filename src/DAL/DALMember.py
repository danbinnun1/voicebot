import sqlite3
import os
import DAL.DALconfig as config
import zipfile

def insertMember(name, password, tone):
    conn = sqlite3.connect(config.progressFilePath)
    c = conn.cursor()
    values = (name, password, tone,)
    c.execute('''
        INSERT INTO members (name, password, progress) VALUES (?,?,?)
        ''', values)
    conn.commit()
    conn.close()
    os.mkdir(os.path.join(config.recordingsFolderPath, name))

def usernameExists(username):
    conn = sqlite3.connect(config.progressFilePath)
    c = conn.cursor()
    searchParameters = (username,)
    searchResult = c.execute('''
        SELECT * FROM members WHERE name=?
        ''', searchParameters).fetchone()
    return searchResult == None

def updateUserProgress(newTone, username):
    conn = sqlite3.connect(config.progressFilePath)
    c = conn.cursor()
    values = (newTone, username)
    c.execute('''
        UPDATE members SET tone=? WHERE name=?
        ''', values)
    conn.commit()
    conn.close()

def memberExists(username, password):
    conn = sqlite3.connect(config.progressFilePath)
    c = conn.cursor()
    searchParameters = (username, password,)
    searchResult = c.execute('''
        SELECT * FROM members WHERE name=? AND password=?
        ''', searchParameters).fetchone()
    return searchResult != None

def zipUserTone(username, tone, outputPath):
    with zipfile.ZipFile(outputPath, mode='w') as zipf:
        dir_path = os.path.join(config.recordingsFolderPath, username, tone)
        len_dir_path = len(dir_path)
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])

def getMemberProgress(username):
    conn = sqlite3.connect(config.progressFilePath)
    c = conn.cursor()
    searchParameters = (username,)
    searchResult = c.execute('''
        SELECT progress FROM members WHERE name=?
        ''', searchParameters).fetchone()
    return searchResult[1]