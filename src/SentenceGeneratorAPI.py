from flask import Flask, send_from_directory, abort, render_template, request, redirect, send_file
import zipfile
import Sentence
import Data
import uuid
import os
import Member
from SoundException import SoundException
import Tone
app = Flask(__name__)


@app.route('/generate_sentence/<speaker>/<sentence>')
def sendSentenceRecording(speaker, sentence):
    temporalName = uuid.uuid4().hex+".mp3"
    temporalFile = Data.temporalFilePath(temporalName)

    try:
        print(sentence)
        print(speaker)
        Sentence.generateSentence(sentence, speaker, temporalFile)
        data = send_from_directory(
            Data._temporalRecordingsFolderPath, temporalName, as_attachment=True)
        os.remove(temporalFile)
        return data
    except SoundException as e:
        print(e.errorCode)
        return str(int(e.errorCode))


@app.route('/sign_member/<name>')
def signMember(name):
    try:
        Member.signMember(name)
        return ""
    except SoundException as e:
        return str(int(e.errorCode))


@app.route('/upload_sound', methods=["POST", "GET"])
def uploadRecording():
    print(request.url)
    if request.method == "POST":
        if request.files:
            try:
                newTone = Tone.nextTone(request.form["tone"])
                recording = request.files["mp3"]
                temporalName = uuid.uuid4().hex
                recording.save(os.path.join(
                    Data.temporalFilePath(temporalName)))
                Member.addRecordings(
                    temporalName, request.form["name"], request.form["tone"])
                return newTone
            except SoundException as error:
                return str(int(error.errorCode))
    return render_template('upload_sound.html')


app.run(debug=True)
