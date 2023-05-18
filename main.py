import cv2 as cv
import numpy as np
import mediapipe as mp
import rotation_debug
#from OpenGL.GL import *
#from OpenGL.GLU import *

cap = cv.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

def normalize(arr):
    return arr / np.linalg.norm(arr)


with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = holistic.process(image)
        #mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        #mp_drawing.draw_landmarks(frame, results.face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION)

        
        if cv.waitKey(1) == ord('q'):
            break
        if results.pose_landmarks and results.face_landmarks:
            # Make Landmark List
            pose_landmarks = []
            for p in results.pose_landmarks.landmark:
                pose_landmarks.append(np.array([p.x,p.y,p.z]))
        
            face_landmarks = []
            for p in results.face_landmarks.landmark:
                face_landmarks.append(np.array([p.x,p.y,p.z]))
            
            # Torso Calculations
            shoulder_arr = np.array([
                pose_landmarks[11][0] - pose_landmarks[12][0],
                pose_landmarks[11][1] - pose_landmarks[12][1]
                ])
            shoulder_arr = shoulder_arr / np.linalg.norm(shoulder_arr)
            shoulder_angle = np.arcsin(shoulder_arr[1]) * (180 / np.pi)

            # Face Calculations
            face_y_axis = np.array([
                face_landmarks[152][0] - face_landmarks[10][0],
                face_landmarks[152][1] - face_landmarks[10][1],
                face_landmarks[152][2] - face_landmarks[10][2]
            ])
            face_x_axis = np.array([
                face_landmarks[454][0] - face_landmarks[234][0],
                face_landmarks[454][1] - face_landmarks[234][1],
                face_landmarks[454][2] - face_landmarks[234][2]
            ])
            face_x_axis = normalize(face_x_axis)
            face_y_axis = normalize(face_y_axis)

            # multiply this stuff by length and width of drawing, then round, thats why line axis ain't showing up
            # do this for debugging to make sure everything is all correct then proceed to iris
            cv.line(frame, (int(face_landmarks[454][0]), int(face_landmarks[454][1])), (int(face_landmarks[234][0]), int(face_landmarks[234][1])), color=(255,255,0))
            cv.line(frame, (int(face_landmarks[152][0]), int(face_landmarks[152][1])), (int(face_landmarks[10][0]), int(face_landmarks[10][1])), color=(255,0,0))
            cv.line(frame, (100,100),(200,200),color=(255,255,255))
            # X ANGLE is Dot product of Y WORLD AXIS and Y RELATIVE AXIS on YZ PLANE
            # Y ANGLE is Dot product of X WORLD AXIS and X RELATIVE AXIS on XZ PLANE
            # Z ANGLE is Dot product of X WORLD AXIS and X RELATIVE AXIS on XY PLANE
            #face_x_angle = np.arccos(np.dot(normalize(np.array([0, face_y_axis[1], face_y_axis[2]])), np.array([0,1,0]))) * (180 / np.pi)
            #face_x_angle = np.arccos(np.dot(normalize(np.array([0, face_y_axis[1], face_y_axis[2]])), np.array([0,0,1]))) * (180 / np.pi) # X ANGLE NEEDS FIXING
            face_x_angle = np.arcsin(face_y_axis[2] * 2) * (180 / np.pi)
            face_y_angle = np.arccos(np.dot(normalize(np.array([face_x_axis[0], 0, face_x_axis[2]])), np.array([1,0,0]))) * (180 / np.pi)
            face_z_angle_x_axis = np.arccos(np.dot(normalize(np.array([face_x_axis[0], face_x_axis[1], 0])), np.array([1,0,0]))) * (180 / np.pi)
            face_z_angle_y_axis = np.arccos(np.dot(normalize(np.array([face_y_axis[0], face_y_axis[1], 0])), np.array([0,1,0]))) * (180 / np.pi)
            
            # Data Output
            print("Torso Angle : " + str(int(shoulder_angle)) + ", Face X: " + str(int(face_x_angle)) + ", Face Y: " + str(int(face_y_angle)) + ", Face Z (X): " + str(int(face_z_angle_x_axis)) + ", Face Z (Y): " + str(int(face_z_angle_y_axis)))
            
            """rotation_debug.reset_image()
            rotation_debug.draw_lines((0,100), tuple((normalize(np.array([face_y_axis[1], face_x_axis[2]])) * 100).astype(int)), offsetX = 100)
            rotation_debug.draw_lines((100,0), tuple((normalize(np.array([face_x_axis[0], face_x_axis[2]])) * 100).astype(int)), offsetX = 300)
            rotation_debug.draw_lines((100,0), tuple((normalize(np.array([face_x_axis[0], face_x_axis[1]])) * 100).astype(int)), offsetX = 500)
            rotation_debug.draw_lines((000,100), tuple((normalize(np.array([face_y_axis[0], face_y_axis[1]])) * 100).astype(int)), offsetX = 700)
            cv.imshow('rotation debug', rotation_debug.image)"""
            # 
            cv.imshow('img', frame)
            

cap.release()
cv.destroyAllWindows()
    