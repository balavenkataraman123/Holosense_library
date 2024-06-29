import cv2
import numpy as np
import mediapipe as mp
from holosense import SpatialTracker

cap = cv2.VideoCapture("/dev/video4")
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
spatial_tracker = SpatialTracker(
    fov=78.5,
    aspectratio=16/9,
    eyedistance=4,
    eyenosedistance=3)

while True:
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            res = spatial_tracker.calculatePosition(face_landmarks)
            print("Coordinates:" + str(res))

    cv2.imshow('preview', image)
    cv2.waitKey(1)
            