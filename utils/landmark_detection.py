import cv2
import dlib
import numpy as np
import os
import pickle


def extract_landmarks(input_path, output_path, save_path):

    predictor = dlib.shape_predictor(
        "/home/zhalok/Desktop/Projects/BangNet/BangNet-Backend/utils/shape_predictor_68_face_landmarks.dat")

    video_capture = cv2.VideoCapture(input_path)
    frameWidth = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    frameHeight = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    frame_counter = 0

    all_landmarks = []

    frameSize = (500, 500)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 25,
                          (int(frameWidth), int(frameHeight)))

    while True:

        ret, frame = video_capture.read()

        print("Processed frame: ", str(frame_counter))

        if not ret:
            break

        frame_counter += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detector = dlib.get_frontal_face_detector()
        faces = detector(gray, 0)

        for face in faces:

            shape = predictor(gray, face)

            landmarks = np.array([[p.x, p.y] for p in shape.parts()])

            all_landmarks.append(landmarks)

            for (x, y) in landmarks:
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    fileObject = open(save_path, 'wb')
    pickle.dump(all_landmarks, fileObject)
    video_capture.release()
    cv2.destroyAllWindows()
    return all_landmarks
