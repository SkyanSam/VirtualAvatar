import glfw
import cv2 as cv
import numpy as np
import mediapipe as mp
import rotation_debug
from OpenGL.GL import *
from OpenGL.GL import shaders
import facedeform
import texture

glfw.init()
gl_window = glfw.create_window(1280, 720, "Virtual Avatar Output", None, None)

if not gl_window:
    glfw.terminate()
    raise Exception("glfw window cannot be created")

glfw.set_window_pos(gl_window, 400, 200)
glfw.make_context_current(gl_window)


"""
vs_shader_src = open("deformshaderv.glsl", "r").read()
fs_shader_src = open("deformshaderf.glsl", "r").read()
program_id = shaders.compileProgram(
    shaders.compileShader(vs_shader_src, GL_VERTEX_SHADER),
    shaders.compileShader(fs_shader_src, GL_FRAGMENT_SHADER),
    validate=False
)

texture.read_texture("skyansam.png")

triangles = [-1.0, -1.0, 0.0,
            1.0, -1.0, 0.0,
            1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0,
            -1.0, 1.0, 0.0,
            1.0, 1.0, 0.0]
 
triangles = np.array(triangles, dtype=np.float32)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, triangles.nbytes, triangles, GL_STATIC_DRAW)
 
position = glGetAttribLocation(program_id, 'position')
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(position)
"""

facedeform.start()
glClearColor(0,0.5,0.5,1)


cap = cv.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

def normalize(arr):
    return arr / np.linalg.norm(arr)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_face_landmarks=True) as holistic:
    while not glfw.window_should_close(gl_window) and cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break
        
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = holistic.process(image)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
        mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(frame, results.face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION)

        
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
            
            # Iris Tracking
            img_w = frame.shape[1]
            img_h = frame.shape[0]
            mesh_pts = np.array([np.multiply([p.x,p.y], [img_w, img_h]).astype(int) for p in results.face_landmarks.landmark])
            #(left_iris_cx, left_iris_cy), left_iris_radius = cv.minEnclosingCircle(mesh_pts[[160,159,158,157,154,153,145,144]])
            #(right_iris_cx, right_iris_cy), right_iris_radius = cv.minEnclosingCircle(mesh_pts[[384,385,386,387,373,374,380,381]])
            (left_iris_cx, left_iris_cy), left_iris_radius = cv.minEnclosingCircle(mesh_pts[[474,475, 476, 477]])
            (right_iris_cx, right_iris_cy), right_iris_radius = cv.minEnclosingCircle(mesh_pts[[469, 470, 471, 472]])
            iris_left_pos = np.array([left_iris_cx, left_iris_cy], dtype=np.int32)
            iris_right_pos = np.array([right_iris_cx, right_iris_cy], dtype=np.int32)
            cv.circle(frame, iris_left_pos, int(left_iris_radius), (255,0,255), 1, cv.LINE_AA)
            cv.circle(frame, iris_right_pos, int(right_iris_radius), (255,255,0), 1, cv.LINE_AA)
            
            mouth_pts = mesh_pts[[80, 88, 310, 318]]
            mouth_x = abs(mouth_pts[0][0] - mouth_pts[2][0])
            mouth_y = abs(mesh_pts[13][1] - mesh_pts[14][1])
            # Data Output
            #print("Mouth X: " + str(mouth_x) + ", Mouth Y: " + str(mouth_y) + ",Torso Angle : " + str(int(shoulder_angle)) + ", Face X: " + str(int(face_x_angle)) + ", Face Y: " + str(int(face_y_angle)) + ", Face Z (X): " + str(int(face_z_angle_x_axis)) + ", Face Z (Y): " + str(int(face_z_angle_y_axis)))
            
            rotation_debug.reset_image()
            rotation_debug.draw_lines((0,100), tuple((normalize(np.array([face_y_axis[1], face_x_axis[2]])) * 100).astype(int)), offsetX = 100)
            rotation_debug.draw_lines((100,0), tuple((normalize(np.array([face_x_axis[0], face_x_axis[2]])) * 100).astype(int)), offsetX = 300)
            rotation_debug.draw_lines((100,0), tuple((normalize(np.array([face_x_axis[0], face_x_axis[1]])) * 100).astype(int)), offsetX = 500)
            rotation_debug.draw_lines((000,100), tuple((normalize(np.array([face_y_axis[0], face_y_axis[1]])) * 100).astype(int)), offsetX = 700)
            cv.imshow('rotation debug', rotation_debug.image)
            # 
            cv.imshow('img', frame)

            # GL

            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            facedeform.update()
            """glUseProgram(program_id)
            iResolution_id = glGetUniformLocation(program_id, "iResolution")
            glUniform2f(iResolution_id, 1280, 720)
            # 960x540, 1280x720, 1600x900, 1920x1080
            glDrawArrays(GL_TRIANGLES, 0, 6)
            glUseProgram(0)"""
            
            print(glGetDebugMessageLog())
            glfw.swap_buffers(gl_window)
            glfw.poll_events()

glfw.terminate()
cap.release()
cv.destroyAllWindows()
    