tonesPath = '../data/tones.txt'

tones = []
with open(tonesPath, 'r') as tonesFile:
    tones = tonesFile.read().split(',')
tonesFile.close()


def firstTone():
    return tones[0]

# -1 means tone1 before tone2
# 0 means they are equal
# 1 means tone1 after tone2


def compareTonesOrder(tone1, tone2):
    if tone1 == tone2:
        return 0
    for tone in tones:
        if tone == tone1:
            return -1
        if tone == tone2:
            return 1


def nextTone(tone):
    for i in range(0, len(tones)):
        if (tones[i] == tone):
            return tones[i+1]
