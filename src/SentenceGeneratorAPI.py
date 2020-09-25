from flask import Flask, send_from_directory, abort, render_template, request, redirect
import Sentence
import Data
import uuid
import os
import Member
from SoundException import SoundException
app = Flask(__name__)


@app.route('/generateSentence/<speaker>/<sentence>')
def sendSentenceRecording(speaker, sentence):
    temporalName = uuid.uuid4().hex
    temporalFile = Data.temporalRecordingsFolderPath+'/' + temporalName

    try:
        print(sentence)
        print(speaker)
        Sentence.generateSentence(sentence, speaker, temporalFile)
        data = send_from_directory(
            Data.temporalRecordingsFolderPath, temporalName, as_attachment=True)
        os.remove(temporalFile)
        return data
    except SoundException as e:
        print(e.errorCode)
        return str(e.errorCode)


@app.route('/sign_member/<name>')
def signMember(name):
    try:
        Member.signMember(name)
        return ""
    except SoundException as e:
        return str(e.errorCode)


@app.route('/upload_sound', methods=["POST", "GET"])
def uploadRecording():
    print(request.url)

    if request.method == "POST":
        print(777)
        if request.files:
            recording = request.files["mp3"]
            temporalName = uuid.uuid4().hex
            recording.save(os.path.join(
                Data.temporalRecordingsFolderPath)+'/'+temporalName)
            try:
                Member.addRecordings(
                    temporalName, request.form["name"], request.form["tone"])
                return request.url
            except SoundException as error:
                return str(error.errorCode)
    return render_template('upload_sound.html')


app.run(debug=True)
