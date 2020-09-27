# Voicebot 🔊
## a bot that lets people make their own voicebots

### error codes
| Error number | Description |
| :----------: | :---------- |
| 0 | the recording file is invalid, it nedds to be mp3 and its content should be syllables padded by 1 second of silence. the syllables amount must be the same as the amount of vowels |
| 1 | the recording tone is after the current user progress |
| 2 | the sentence is invalid |
| 3 | trying to add username the already exists |
| 4 | try to access user that does not exist |
| 5 | trying to add tone that does not exists |
| 6 | trying to get sentence from user who did not finished registaration |

## 📌 Endpoints:

### `GET /sign_member/<name>`
creates a new member with name `<name>`, note that member names are unique. 
Example: `GET /sign_member/Amit`

### `GET /generate_sentence/<speaker>/<sentence>`
generates a sentence with speaker `<speaker>` and sentence `<sentence>` according to the [sentence format](#-sentence-format)
Example: `GET /generate_sentence/Amit/yes.`

### `POST /upload_sound`
endpoint that has an html form that lets you upload a file, you must specify name of member and the sound to upload
Example: `GET /upload_sound`

### `GET /members`
return json format of all members and their progress
Example: `GET /members`

### `GET /members/<name>`
return the progress of a certain member, if the member doen not exist it returns error code
Example: `GET /members/heni`

### ✅ Sentence format:
`(<tone><vowel>)(<tone><vowel>)(<tone><vowel>)....`
example:
`kakipipitusik.bul.bul.`
