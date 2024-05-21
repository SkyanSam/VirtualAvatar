
import cv2 as cv
import numpy as np
import mediapipe as mp
import rotation_debug
import headposeestimation

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
    holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.9, refine_face_landmarks=True)

def normalize(arr):
    return arr / np.linalg.norm(arr)

def is_window_open():
    global cap
    return cap.isOpened() and cv.waitKey(1) != ord('q')

def update():
    global cap
    global mp_drawing
    global mp_holistic
    global holistic
    global face_x_angle
    global head_angle_x, head_angle_y, head_angle_z
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
        
        # Iris Tracking
        img_w = frame.shape[1]
        img_h = frame.shape[0]
        mesh_pts = np.array([np.multiply([p.x,p.y], [img_w, img_h]).astype(int) for p in results.face_landmarks.landmark])
        (left_iris_cx, left_iris_cy), left_iris_radius = cv.minEnclosingCircle(mesh_pts[[474,475, 476, 477]])
        (right_iris_cx, right_iris_cy), right_iris_radius = cv.minEnclosingCircle(mesh_pts[[469, 470, 471, 472]])
        iris_left_pos = np.array([left_iris_cx, left_iris_cy], dtype=np.int32)
        iris_right_pos = np.array([right_iris_cx, right_iris_cy], dtype=np.int32)
        cv.circle(frame, iris_left_pos, int(left_iris_radius), (255,0,255), 1, cv.LINE_AA)
        cv.circle(frame, iris_right_pos, int(right_iris_radius), (255,255,0), 1, cv.LINE_AA)
        
        # eyelid_(left/right)_y should give values from 0.0 to 1.0
        # may need to adjust, note that the raw ratio values before subtraction/multiplication is from 0.1 to 0.4
        eye_left_length = abs(mesh_pts[133][0] - mesh_pts[33][0])
        eye_right_length = abs(mesh_pts[362][0] - mesh_pts[263][0])
        eyelid_left_y = ((abs(mesh_pts[159][1] - mesh_pts[145][1]) / eye_left_length) - 0.1) * 3.3
        eyelid_right_y = ((abs(mesh_pts[374][1] - mesh_pts[386][1]) / eye_right_length) - 0.1) * 3.3
    
        # iris
        # note for y get difference between iris y and eye left/right center y..
        # get normalized values..
        eye_left_center = (mesh_pts[133] + mesh_pts[33]) / 2.0
        eye_right_center = (mesh_pts[362] + mesh_pts[263]) / 2.0

        # Mouth
        mouth_pts = mesh_pts[[80, 88, 310, 318]]
        mouth_x = abs(mouth_pts[0][0] - mouth_pts[2][0])
        mouth_y = abs(mesh_pts[13][1] - mesh_pts[14][1])
        # Data Output
        print("Eyelid: " + str(eyelid_left_y) + ", " + str(eyelid_right_y))
        #print("Mouth X: " + str(mouth_x) + ", Mouth Y: " + str(mouth_y) + ",Torso Angle : " + str(int(shoulder_angle)) + ", Face X: " + str(int(head_angle_x)) + ", Face Y: " + str(int(head_angle_y)) + ", Face Z: " + str(int(head_angle_z)))
        
        cv.imshow('img', frame)
    else:
        print("no landmarks for cv")

def end():
    cap.release()
    cv.destroyAllWindows()
    