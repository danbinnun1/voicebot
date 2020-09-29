from SoundError import SoundError
from SoundException import SoundException

_tonesPath = '../settings/tones.txt'

tones = []
with open(_tonesPath, 'r') as tonesFile:
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
    for i in range(0, len(tones)-1):
        if (tones[i] == tone):
            return tones[i+1]
    raise SoundException(
        SoundError.TONE_DOES_NOT_EXIST)


# checks weather the current progress means 'done'
def finishedRegisteration(tone):
    return tone == tones[-1]
