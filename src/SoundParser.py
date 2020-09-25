
from pydub import AudioSegment
from pydub.silence import split_on_silence
import Vowel
import os
import SoundError
import SoundException
import shutil

def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

import Data
sourceFolder = Data.temporalRecordingsFolderPath+'/'


def splitSound(filePath, outputPath):
    audio = AudioSegment.from_mp3(sourceFolder + filePath)
    chunks = split_on_silence(
        # Use the loaded audio.
        audio,
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len=500,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh=-45
    )
    if len(Vowel.vowels) != len(chunks):
        raise SoundException.SoundException(
            SoundError.SoundError.INVALID_RECORDING_FILE)
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
    os.makedirs(outputPath)
    #os.mkdir(outputPath)
    for i, chunk in enumerate(chunks):
        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(chunk, -20.0)
        # Export the audio chunk with new bitrate.
        normalized_chunk.export(
            outputPath+'/'+Vowel.vowels[i]+'.mp3',
            bitrate="192k",
            format="mp3"
        )

# splitSound('g.mp3','.')
