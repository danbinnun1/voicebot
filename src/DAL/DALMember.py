import sqlite3
import os
import DAL.DALconfig as config

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

def usernameAvailable(username):
    conn = sqlite3.connect(config.progressFilePath)
    c = conn.cursor()
    searchParameters = (username,)
    searchResult = c.execute('''
        SELECT * FROM members WHERE name=?
        ''', searchParameters).fetchone()
    return searchResult == None

def uploadVowelRecording(recording, username, tone, vowel):
    recording.export(
        os.path.join(config.recordingsFolderPath,username,tone,vowel),
        bitrate="192k",
        format="mp3"
    )

def updateUserProgress(newTone, username):
    conn = sqlite3.connect(config.progressFilePath)
    c = conn.cursor()
    values = (newTone, username)
    c.execute('''
        UPDATE members SET tone=? WHERE name=?
        ''', values)
    conn.commit()
    conn.close()