from flask import Flask, send_from_directory, abort
import Sentence
import Data
import uuid
import os
from SoundException import SoundException
app = Flask(__name__)


@app.route('/generateSentence/<speaker>/<sentence>')
def sendSentenceRecording(speaker, sentence):
    temporalName=uuid.uuid4().hex
    temporalFile = Data.temporalRecordingsFolderPath+'/' + temporalName

    try:
        print(sentence)
        print(speaker)
        Sentence.generateSentence(sentence, speaker, temporalFile)
        data= send_from_directory(Data.temporalRecordingsFolderPath, temporalName, as_attachment=True)
        os.remove(temporalFile)
        return data
    except SoundException as e:
        return str(e.errorCode)

app.run()