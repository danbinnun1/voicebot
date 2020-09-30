
from pydub.silence import split_on_silence
from BL.SoundError import SoundError
from BL.SoundException import SoundException
from BL.BLconfig import vowels

def _match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


def splitSound(audio):
    try:
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
    for i, chunk in enumerate(chunks):
        chunk = _match_target_amplitude(chunk, -20.0)
        chunks[i] = chunk[0:300]
    return chunks