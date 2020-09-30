_vowelsPath = '/home/danbinnun1/voicebot/settings/vowels.txt'
_tonesPath = '/home/danbinnun1/voicebot/settings/tones.txt'

with open(_vowelsPath, 'r') as vowelsFile:
    vowels = vowelsFile.read().split(',')
vowelsFile.close()
with open(_tonesPath, 'r') as tonesFile:
    tones = tonesFile.read().split(',')
tonesFile.close()
print(tones)
