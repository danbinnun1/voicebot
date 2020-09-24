from pydub import AudioSegment


def generateSentence(sentenceString, speaker, outputPath):
    folderPath = '../data/' + speaker+'/'
    i = 0
    sentenceAudio = AudioSegment.silent(0)
    while i < len(sentenceString):
        vowel = sentenceString[i:i+2]
        sentenceAudio = sentenceAudio + AudioSegment.from_mp3(folderPath+vowel+'.mp3')
        i += 2
    sentenceAudio.export(
        outputPath,
        bitrate="192k",
        format="mp3"
    )