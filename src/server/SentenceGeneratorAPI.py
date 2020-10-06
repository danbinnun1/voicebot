import sys
sys.path.append('.')

import os
import uuid
from flask import Flask, jsonify, send_from_directory, abort, render_template, request, redirect, send_file, safe_join
import src.BL.BLconfig as config
from src.BL.SoundError import SoundError
from src.BL.Member import Member
from pydub import AudioSegment
from src.BL.SoundException import SoundException
from src.BL import Data
import sys
sys.path.append('.')


Data.initializeData()
app = Flask(__name__)


@app.route('/generate_sentence/<speakerUsername>/<sentence>')
def sendSentenceRecording(speakerUsername, sentence):
    try:
        temporalName = uuid.uuid4().hex+".mp3"
        speaker = Member.getMemberByusername(speakerUsername)
        sentenceAudio = speaker.generateSentence(sentence)
        filename = uuid.uuid4().hex+'.mp3'
        sentenceAudio.export(
            filename,
            bitrate="192k",
            format="mp3"
        )
        data = send_from_directory('../..', filename,
                                   as_attachment=True)
        os.remove(filename)
        return data
    except SoundException as e:
        return str(int(e.errorCode))


@app.route('/sign_up', methods=["POST", "GET"])
def signMember():
    if request.method == "POST":
        try:
            newMember = Member.initializeMember(
                request.form["username"], request.form["password"])
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
                uploader = Member.getMemberBynameAndPassword(
                    request.form["name"], request.form["password"])
                uploader.uploadSound(AudioSegment.from_file(
                    recordingPath), request.form["tone"])
                zipfilePath = uuid.uuid4().hex+'.zip'
                uploader.zipTone(request.form["tone"], zipfilePath)
                data = send_file(
                    '../../'+zipfilePath,
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
    return Member.getAllMembers()


@app.route('/members/<name>')
def getProgress(name):
    try:
        member = Member.getMemberByusername(name)
        return str(member.getProgress())
    except SoundException as e:
        return str(int(e.errorCode))


@app.route('/vowels')
def getVowels():
    return str(config.vowels)


app.run(debug=True)
