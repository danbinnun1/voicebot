import os
import Tone
import shutil
import SoundParser

progressPath = '../data/progress.txt'
recordingsPath = '../data/recordings/'
progressFileContent = ''
with open(progressPath, 'r') as file:
    progressFileContent = file.read()
file.close()
members = {}
membersStrings = progressFileContent.split('\n')
for s in membersStrings[0:len(membersStrings)-1]:
    members[s.split(',')[0]] = s.split(',')[1]


def signMember(name):
    with open(progressPath, 'a+') as file:
        file.write(name+','+Tone.firstTone()+'\n')
    os.mkdir(recordingsPath+name)
    file.close()
    members[name] = Tone.firstTone()


def addRecordings(recording, memberName, tone):
    currentTone = members[memberName]
    tonesOrder = Tone.compareTonesOrder(tone, currentTone)
    outputPath = recordingsPath+memberName+'/'+tone
    # this is a repair of existing tone
    if tonesOrder == -1:
        os.rmdir(outputPath)
        SoundParser.splitSound(recording, outputPath)
    elif tonesOrder == 0:
        members[memberName] = Tone.nextTone(members[memberName])
        rows = []
        with open(progressPath, 'r') as file:
            rows = file.read().split('\n')
        file.close()
        newRows = []
        for row in rows:
            if row.split(',')[0] == memberName:
                newRows.append(memberName+','+Tone.nextTone(row.split(',')[1]))
            else:
                newRows.append(row)
        with open(progressPath, 'w') as file:
            for row in newRows[0:len(rows)-1]:
                file.write(row+'\n')
        file.close()
        SoundParser.splitSound(recording, outputPath)
    else:
        raise Exception("sent recording after current")
