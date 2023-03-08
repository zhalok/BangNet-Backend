import firebase_admin
from firebase_admin import *


config = {"apiKey": "AIzaSyBtM0Gz6MgFElP5QZmu58A3R2Mxs5GV6XA", "authDomain": "lipread-2718a.firebaseapp.com", "databaseURL": "https://lipread-2718a-default-rtdb.firebaseio.com",
          "projectId": "lipread-2718a", "storageBucket": "lipread-2718a.appspot.com", "messagingSenderId": "684508315801", "appId": "1:684508315801:web:4f96efc36b696b59233808", "measurementId": "G-GH5JN8J8BD"}

cred = credentials.Certificate(
    "/home/zhalok/Desktop/Projects/BangNet/BangNet-Backend/utils/credentials/lipread-2718a-firebase-adminsdk-ubp6t-3981542907.json")


# print(cred)
firebase_app = firebase_admin.initialize_app(cred, config)

# from firebase_admin import
