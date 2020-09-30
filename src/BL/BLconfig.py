_vowelsPath = '/home/danbinnun1/voicebot/settings/vowels.txt'

vowels = []


_tonesPath = '/home/danbinnun1/voicebot/settings/tones.txt'
tones = []


def _parseSettings():
    with open(_vowelsPath, 'r') as vowelsFile:
        vowels = vowelsFile.read().split(',')
    vowelsFile.close()
    with open(_tonesPath, 'r') as tonesFile:
        tones = tonesFile.read().split(',')
    tonesFile.close()

_parseSettings()