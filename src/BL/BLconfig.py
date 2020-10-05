_vowelsPath = './settings/vowels.txt'
_tonesPath = './settings/tones.txt'

class BLconfig:
    __vowels=None
    __tones=None
    @staticmethod
    def getVowels():
        if BLconfig.__vowels==None:
            with open(_vowelsPath, 'r') as vowelsFile:
                BLconfig.__vowels = vowelsFile.read().split(',')
            vowelsFile.close()
        return BLconfig.__vowels

    @staticmethod
    def getTones():
        if BLconfig.__tones==None:
            with open(_tonesPath, 'r') as tonesFile:
                BLconfig.__tones = tonesFile.read().split(',')
            tonesFile.close()
        return BLconfig.__tones