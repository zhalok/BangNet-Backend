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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HELLO WORLD')
ALLOWED_EXTENSIONS = set(['mp4', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__, static_folder='./static')
port = 5000
CORS(app, support_credentials=True)

UPLOAD_FOLDER = './static/uploads/'
OUTPUT_FOLDER = './static/landmarks/'


@app.route("/", methods=["GET", "POST"])
def hello_world():

    return {"message": "hello world"}


@app.route("/contribute", methods=['POST', 'GET'])
def detect_landmark():
    target = os.path.join(UPLOAD_FOLDER, '.')
    landmark_output = os.path.join(OUTPUT_FOLDER, '.')
    file = request.files['file']
    label = request.form.get("label")
    contributor_name = request.form.get("contributor_name")
    contributor_email = request.form.get("contributor_email")
    filename = request.form.get('name')
    destination = "/".join([target, filename+".mp4"])
    # print(type(filename))
    file.save(destination)
    landmark_file_path = os.path.join(
        "/home/zhalok/Desktop/Projects/BangNet/BangNet-Backend/static/landmarks", str(filename)+".pkl")
    landmark_file_blob = os.path.join("landmarks", label, filename+".pkl")
    landmark_video_blob = os.path.join("landmarks", label, filename+".avi")
    landmark_video_file = os.path.join(
        "/home/zhalok/Desktop/Projects/BangNet/BangNet-Backend/landmark_clips", str(filename)+".avi")
    extract_landmarks(destination, landmark_video_file, landmark_file_path)
    file_url = file_upload(landmark_file_blob, landmark_file_path)
    video_url = file_upload(landmark_video_blob, landmark_video_file)

#  detect_landmark()

    return {"file": file_url, "video": video_url}
