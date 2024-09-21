import face_recognition
import os
import cv2
import numpy as np

FACES_DIR = 'authentication/biometrics/'
TOLERANCE = 0.6
MODEL = 'hog'

known_faces = []
known_names = []

for name in os.listdir(FACES_DIR):
    for filename in os.listdir(f'{FACES_DIR}/{name}'):
        image = face_recognition.load_image_file(f'{FACES_DIR}/{name}/{filename}')
        try:
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(name)
        except IndexError:
            continue

known_faces = np.array(known_faces)

def validate(id, img):
    image = face_recognition.load_image_file(img)
    locations = face_recognition.face_locations(image, model=MODEL)
    if not locations: return False
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.RGB2BGR)
    for face_encoding in encodings:
        distances = face_recognition.face_distance(known_faces, face_encoding)
        results = distances <= TOLERANCE
        match = None
        if any(results):
            match = known_names[np.argmin(distances)]
            try:
                assert match==id
            except AssertionError:
                print(f"{match} != {id}")
            if match==id:
                return True
    return False

if __name__=='__main__':
    print(validate('KID4869832', 'uploads/ABC1234567_capture.jpg'))
    print(validate('ABC1234567', 'uploads/ABC1234567_capture.jpg'))