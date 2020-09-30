_vowelsPath = '/home/danbinnun1/voicebot/settings/vowels.txt'

vowels = []
with open(_vowelsPath, 'r') as vowelsFile:
    vowels = vowelsFile.read().split(',')
vowelsFile.close()
