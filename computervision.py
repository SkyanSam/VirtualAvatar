
import cv2 as cv
import numpy as np
import mediapipe as mp
import rotation_debug
import headposeestimation
from faceexpressiondata import *

face_expression_data = None
face_x_angle = 0.0
head_angle_x = 0.0
head_angle_y = 0.0
head_angle_z = 0.0
def start():
    global cap
    global mp_drawing
    global mp_holistic
    global holistic
    cap = cv.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_face_landmarks=True)

def normalize(arr):
    return arr / np.linalg.norm(arr)

def is_window_open():
    global cap
    return cap.isOpened() and cv.waitKey(1) != ord('q')

def update():
    # Mediapipe
    global cap
    global mp_drawing
    global mp_holistic
    global holistic
    # Necessary Positions & Rotation Values
    global face_x_angle
    global head_angle_x, head_angle_y, head_angle_z
    global shoulder_angle
    global face_expression_data

    ret, frame = cap.read()
    if not ret:
        print("CV RETURNING not ret")
        return
    
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = holistic.process(image)
    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
    mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(frame, results.face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION)
    
    if results.pose_landmarks and results.face_landmarks:
        # Make Landmark List
        pose_landmarks = []
        for p in results.pose_landmarks.landmark:
            pose_landmarks.append(np.array([p.x,p.y,p.z]))
    
        face_landmarks = []
        for p in results.face_landmarks.landmark:
            face_landmarks.append(np.array([p.x,p.y,p.z]))
        
        # Head Pose Calculations
        head_angle_x, head_angle_y, head_angle_z = headposeestimation.estimate(results.face_landmarks.landmark, image.shape[0], image.shape[1])

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
        
        # Mesh Points
        img_w = frame.shape[1]
        img_h = frame.shape[0]
        mesh_pts = np.array([np.multiply([p.x,p.y], [img_w, img_h]).astype(int) for p in results.face_landmarks.landmark])
        
        
        # eyelid_(left/right)_y should give values from 0.0 to 1.0
        # may need to adjust, note that the raw ratio values before subtraction/multiplication is from 0.1 to 0.4
        eye_left_length = abs(mesh_pts[133][0] - mesh_pts[33][0])
        eye_right_length = abs(mesh_pts[362][0] - mesh_pts[263][0])
        eye_overall_length = (eye_left_length + eye_right_length) / 2.0
        eyelid_left_y = ((abs(mesh_pts[159][1] - mesh_pts[145][1]) / eye_left_length) - 0.1) * 3.3
        eyelid_right_y = ((abs(mesh_pts[374][1] - mesh_pts[386][1]) / eye_right_length) - 0.1) * 3.3

        # iris
        # note for y get difference between iris y and eye left/right center y..
        # get normalized values..
        # note that iris_right_pos is left pos because flipped (depending on audience view or no)
        eye_left_center = (mesh_pts[133] + mesh_pts[33]) / 2.0
        eye_right_center = (mesh_pts[362] + mesh_pts[263]) / 2.0
        (left_iris_cx, left_iris_cy), left_iris_radius = cv.minEnclosingCircle(mesh_pts[[474,475, 476, 477]])
        (right_iris_cx, right_iris_cy), right_iris_radius = cv.minEnclosingCircle(mesh_pts[[469, 470, 471, 472]])
        iris_left_pos = np.array([left_iris_cx, left_iris_cy], dtype=np.int32)
        iris_right_pos = np.array([right_iris_cx, right_iris_cy], dtype=np.int32)
        cv.circle(frame, iris_left_pos, int(left_iris_radius), (255,0,255), 1, cv.LINE_AA)
        cv.circle(frame, iris_right_pos, int(right_iris_radius), (255,255,0), 1, cv.LINE_AA)
        # note, we flip the left and right data here. (may want to reconsider this behaviour)
        iris_left_normalized = (iris_right_pos - eye_left_center) / 1
        iris_right_normalized = (iris_left_pos - eye_right_center) / 1

        # Mouth
        mouth_pts = mesh_pts[[80, 88, 310, 318]]
        mouth_x = abs(mouth_pts[0][0] - mouth_pts[2][0]) / eye_overall_length
        mouth_y = abs(mesh_pts[13][1] - mesh_pts[14][1]) / eye_overall_length

        # Eyebrow, note that if you aren't getting strong results replace the points with a different portion of the eyebrow.
        eyebrow_left = (mesh_pts[105][1] - mesh_pts[104][1]) / abs(mesh_pts[104][1] - mesh_pts[103][1])
        eyebrow_right = (mesh_pts[334][1] - mesh_pts[333][1]) / abs(mesh_pts[333][1] - mesh_pts[332][1])
        
        # NOTE TO SELF NORMALIZE THE MOUTH DATA
        # Data Output
        #print("EyeLeft: " + str(round(iris_left_normalized[0], 2)) + ", " + str(round(iris_left_normalized[1], 2)) + ": EyeRight: " + str(round(iris_right_normalized[0], 2)) + ", " + str(round(iris_right_normalized[1], 2)))
        print("Mouth X: " + str(mouth_x) + ", Mouth Y: " + str(mouth_y) + ",Torso Angle : " + str(int(shoulder_angle)) + ", Face X: " + str(int(head_angle_x)) + ", Face Y: " + str(int(head_angle_y)) + ", Face Z: " + str(int(head_angle_z)))
        
        face_expression_data = FaceExpressionData(
            eyebrow_left = eyebrow_left,
            eyebrow_right = eyebrow_right,
            left_eye_open = eyelid_left_y,
            right_eye_open = eyelid_right_y,
            left_iris_x = iris_left_normalized[0],
            left_iris_y = iris_left_normalized[1],
            right_iris_x = iris_right_normalized[0],
            right_iris_y = iris_right_normalized[1],
            mouth_open_x = mouth_x,
            mouth_open_y = mouth_y
        )
        cv.imshow('img', frame)
    else:
        print("no landmarks for cv")

def end():
    cap.release()
    cv.destroyAllWindows()
    