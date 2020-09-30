import DAL.DALconfig as config
import os
from pydub import AudioSegment


def uploadVowelRecording(recording, username, tone, vowel):
    recording.export(
        os.path.join(config.recordingsFolderPath, username, tone, vowel),
        bitrate="192k",
        format="mp3"
    )


def getVowelRecording(username, tone, vowel):
    return AudioSegment.from_mp3(os.path.join(
        config.recordingsFolderPath, username, tone, vowel) + '.mp3')
