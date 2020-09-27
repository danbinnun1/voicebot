# Voicebot 🔊
### a bot that lets people make their own voicebots

error code:
    the recording file is invalid, it nedds to be mp3 and its content should
    be syllables padded by 1 second of silence. the syllables amount must be the same as the amount of vowels = 0
    the recording tone is after the current user progress = 1
    the sentence is invalid = 2
    trying to add username the already exists = 3
    try to access user that does not exist = 4
    trying to add tone that does not exists = 5
    trying to get sentence from user who did not finished registaration = 6

## 📌 Endpoints:

### `GET /sign_member/<name>`
creates a new member with name `<name>`, note that member names are unique. 

### `GET /generate_sentence/<speaker>/<sentence>`
generates a sentence with speaker `<speaker>` and sentence `<sentence>` according to the [sentence format](#-sentence-format)

### `GET /upload_sound`
endpoint that has an html form that lets you upload a file, you must specify name of member and the sound to upload

### ✅ Sentence format:
`(<tone><vowel>)(<tone><vowel>)(<tone><vowel>)....`
example:
`kakipipitusik.bul.bul.`
