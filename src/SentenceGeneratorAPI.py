from SoundError import SoundError
from flask import Flask, jsonify, send_from_directory, abort, render_template, request, redirect, send_file
import zipfile
import Sentence
import Data
import uuid
import os
import Vowel
import Member
from SoundException import SoundException
import Tone
app = Flask(__name__)


@app.route('/generate_sentence/<speaker>/<sentence>')
def sendSentenceRecording(speaker, sentence):
    temporalName = uuid.uuid4().hex+".mp3"

    try:
        print(sentence)
        print(speaker)
        Sentence.generateSentence(sentence, speaker, os.path.join(
            Data.temporalRecordingsFolderPath, temporalName))
        data = send_from_directory(
            Data.temporalRecordingsFolderPath, temporalName, as_attachment=True)
        os.remove(os.path.join(Data.temporalRecordingsFolderPath, temporalName))
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
            temporalName = uuid.uuid4().hex
            try:
                recording = request.files["mp3"]
                recording.save(os.path.join(
                    Data.temporalRecordingsFolderPath, temporalName))
                Member.addRecordings(
                    os.path.join(Data.temporalRecordingsFolderPath, temporalName), request.form["name"], request.form["tone"])
                userToneZipFileName = uuid.uuid4().hex+'.zip'
                Data.zipUserTone(
                    request.form["name"], request.form["tone"], os.path.join(Data.temporalRecordingsFolderPath, userToneZipFileName))
                data = send_file(
                    os.path.join(Data.temporalRecordingsFolderPath,
                                 userToneZipFileName),
                    mimetype='zip',
                    attachment_filename=userToneZipFileName,
                    as_attachment=True
                )
                os.remove(os.path.join(
                    Data.temporalRecordingsFolderPath, userToneZipFileName))
                os.remove(os.path.join(
                    Data.temporalRecordingsFolderPath, temporalName))
                return data
            except SoundException as error:
                os.remove(os.path.join(
                    Data.temporalRecordingsFolderPath, temporalName))
                return str(int(error.errorCode))

    return render_template('upload_sound.html')


@app.route('/members')
def members():
    return Member.members


@app.route('/members/<name>')
def getProgress(name):
    if (name in Member.members):
        return str(Member.members[name])
    return str(int(SoundError.USERNAME_DOES_NOT_EXIST))


@app.route('/vowels')
def getVowels():
    return jsonify({'response': Vowel.vowels})


app.run(debug=True)
