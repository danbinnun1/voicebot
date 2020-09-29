
import Data
from pydub import AudioSegment
from pydub.silence import split_on_silence
import Vowel
import os
from SoundError import SoundError
from SoundException import SoundException
import shutil

def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def splitSound(filePath, filename):
    try:
        audio = AudioSegment.from_file(Data.temporalFilePath(filePath))
        chunks = split_on_silence(
            audio,
            min_silence_len=500,
            silence_thresh=-30
        )
    except Exception as e:
        print(e)
        raise SoundException(SoundError.INVALID_RECORDING_FILE)
    if len(Vowel.vowels) != len(chunks):
        print(len(Vowel.vowels), len(chunks))
        raise SoundException(SoundError.INVALID_RECORDING_FILE)
    if os.path.exists(filename):
        shutil.rmtree(filename)
    os.makedirs(filename)
    for i, chunk in enumerate(chunks):
        normalized_chunk = match_target_amplitude(chunk, -20.0)
        trimmed_chunk=normalized_chunk[0:300]
        trimmed_chunk.export(
            filename+'/'+Vowel.vowels[i]+'.mp3',
            bitrate="192k",
            format="mp3"
        )