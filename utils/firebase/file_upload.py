import firebase_admin
from utils.firebase.admin import firebase_app
from firebase_admin import storage
# from blob_metadata import blob_metadata


def file_upload(blob_name, file_path):
    bucket = storage.bucket()
    blob = bucket.blob(blob_name)
    with open(file_path, 'rb') as my_file:
        blob.upload_from_file(my_file)
        blob.make_public()
        # print(blob.public_url)
        return blob.public_url
