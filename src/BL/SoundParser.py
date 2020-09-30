
from pydub import AudioSegment
from pydub.silence import split_on_silence
from Vowel import vowels
import os
from SoundError import SoundError
from SoundException import SoundException
import shutil


def _match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


def splitSound(inputFilePath, outputFolderPath):
    try:
        audio = AudioSegment.from_file(inputFilePath)
        chunks = split_on_silence(
            audio,
            min_silence_len=500,
            silence_thresh=-30
        )
    except Exception as e:
        print(e)
        raise SoundException(SoundError.INVALID_RECORDING_FILE)
    if len(vowels) != len(chunks):
        print(len(vowels), len(chunks))
        raise SoundException(SoundError.INVALID_RECORDING_FILE)
    if os.path.exists(outputFolderPath):
        shutil.rmtree(outputFolderPath)
    os.makedirs(outputFolderPath)
    for i, chunk in enumerate(chunks):
        normalized_chunk = _match_target_amplitude(chunk, -20.0)
        trimmed_chunk = normalized_chunk[0:300]
        trimmed_chunk.export(
            os.path.join(outputFolderPath, vowels[i]+'.mp3'),
            bitrate="192k",
            format="mp3"
        )
