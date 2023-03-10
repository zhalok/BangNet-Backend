import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from glob import glob
import logging
import threading
from utils.firebase.admin import firebase_app
from utils.landmark_detection import extract_landmarks
from utils.firebase.file_upload import file_upload
from firebase_admin import firestore
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HELLO WORLD')
ALLOWED_EXTENSIONS = set(['mp4', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__, static_folder='./static')
port = 5000
CORS(app, support_credentials=True)

UPLOAD_FOLDER = './static/uploads/'
OUTPUT_FOLDER = './static/landmarks/'
root = os.path.abspath(os.curdir)


@app.route("/", methods=["GET", "POST"])
def hello_world():

    return {"message": "hello world"}


@app.route("/contribute", methods=['POST', 'GET'])
def contribute():
    target = os.path.join(UPLOAD_FOLDER, '.')
    landmark_output = os.path.join(OUTPUT_FOLDER, '.')
    file = request.files['file']
    label = request.form.get("label")
    contributor_name = request.form.get("contributor_name")
    contributor_email = request.form.get("contributor_email")
    filename = request.form.get('name')
    print(label)
    print(contributor_email)
    print(contributor_name)
    db = firestore.client()
    data = {
        u'contributor': contributor_name,
        u'email': contributor_email,
        u'label': label,
        u'date': datetime.datetime.now().strftime("%d/%m/%Y")
    }
    update_time, data_ref = db.collection(u'collections').add(data)

    filename = data_ref.id

    data_path = "/".join([target, filename+".mp4"])

    data_name = os.path.join("collections", label, str(filename)+".mp4")
    landmark_file_path = os.path.join(
        root + "/static/landmarks", str(filename)+".pkl")
    landmark_file_blob = os.path.join(
        "landmarks", label, filename+".pkl")
    landmark_video_blob = os.path.join(
        "landmark_videos", label, filename+".mp4")
    landmark_video_path = os.path.join(
        root + "/landmark_clips", str(filename)+".mp4")

    file.save(data_path)
    extract_landmarks(data_path, landmark_video_path, landmark_file_path)
    print("Uploading landmarks")
    file_url = file_upload(landmark_file_blob, landmark_file_path)
    print("uploading landmark video")
    video_url = file_upload(landmark_video_blob, landmark_video_path)
    print("Uploading collections")
    data_url = file_upload(data_name, data_path)
    print("Upload successful")

    if os.path.exists(data_path):
        os.remove(data_path)
    if os.path.exists(landmark_file_path):
        os.remove(landmark_file_path)
    if os.path.exists(landmark_video_path):
        os.remove(landmark_video_path)
    data["landmark"] = file_url
    data["landmark_video"] = video_url
    data["clip"] = data_url
    db.collection(u'collections').document(filename).set(data)
    return data

