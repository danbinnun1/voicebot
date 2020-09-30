from enum import IntEnum


class SoundError(IntEnum):
    INVALID_RECORDING_FILE = 0
    SENT_RECORDING_AFTER_PROGRESS = 1
    INVALID_SENTENCE = 2
    USERNAME_TAKEN = 3
    USERNAME_DOES_NOT_EXIST = 4
    TONE_DOES_NOT_EXIST = 5
    USER_NOT_FINISHED_REGISTERETION = 6,
    WRONG_USERNAME_OR_PASSWORD = 7,