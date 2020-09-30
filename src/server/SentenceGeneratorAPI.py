import sys
sys.path.append('../')

import BL.Data
from BL.Tone import Tone
from BL.SoundException import SoundException
from pydub import AudioSegment
import BL.Member
from BL.Member import Member
from BL.SoundError import SoundError
from flask import Flask, jsonify, send_from_directory, abort, render_template, request, redirect, send_file
import uuid
import os

BL.Data.initializeData()
app = Flask(__name__)


@app.route('/generate_sentence/<speakerUsername>/<sentence>')
def sendSentenceRecording(speakerUsername, sentence):
    try:
        temporalName = uuid.uuid4().hex+".mp3"
        speaker = BL.Member.getMemberByusername(speakerUsername)
        sentenceAudio = speaker.generateSentence(sentence)
        filename = uuid.uuid4().hex
        data = send_file(sentenceAudio.raw_data, 'audio/mp3',
                         as_attachment=True, attachment_filename=filename)
        return data
    except SoundException as e:
        return str(int(e.errorCode))


@app.route('/sign_up', methods=["POST", "GET"])
def signMember():
    if request.method == "POST":
        try:
            newMember = Member(request.form["username"], Tone.first())
            newMember.save(request.form["password"])
            return ""
        except SoundException as e:
            return str(int(e.errorCode))
    return render_template("sign_member.html")


@app.route('/upload_sound', methods=["POST", "GET"])
def uploadRecording():
    print(request.url)
    if request.method == "POST":
        if request.files:
            try:
                recordingPath = uuid.uuid4().hex
                recording = request.files["mp3"]
                recording.save(recordingPath)
                uploader = BL.Member.getMemberBynameAndPassword(
                    request.form["name"], request.form["password"])
                uploader.uploadSound(AudioSegment.from_file(
                    recordingPath), Tone(request.form["tone"]))
                zipfilePath = uuid.uuid4().hex+'.zip'
                uploader.zipTone(request.form["tone"], zipfilePath)
                data = send_file(
                    zipfilePath,
                    mimetype='zip',
                    attachment_filename=zipfilePath,
                    as_attachment=True
                )
                os.remove(recordingPath)
                os.remove(zipfilePath)
                return data
            except SoundException as error:
                os.remove(recordingPath)
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
