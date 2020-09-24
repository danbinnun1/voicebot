vowelsPath = '../data/vowels.txt'

vowels = []
with open(vowelsPath, 'r') as vowelsFile:
    vowels = vowelsFile.read().split(',')
vowelsFile.close()
