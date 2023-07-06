import numpy as np
import cv2 as cv
def estimate(landmarks, img_w, img_h):
    face_2d = []
    face_3d = []
    for idx, lm in enumerate(landmarks):
        x,y = int(lm.x * img_w), int(lm.y * img_h)
        face_2d.append([x,y])
        face_3d.append([x,y,lm.z])
    
    face_2d = np.array(face_2d, dtype=np.float64)
    face_3d = np.array(face_3d, dtype=np.float64)
    focal_length = 1 * img_w
    cam_matrix = np.array(
        [
            [focal_length, 0, img_h / 2],
            [0, focal_length, img_w / 2],
            [0,0,1]
        ]
    )
    dist_matrix = np.zeros((4,1),dtype=np.float64)

    success, rot_vec, trans_vec = cv.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
    rmat, jac = cv.Rodrigues(rot_vec)
    angles, mtxR, mtxQ, Qx, Qy, Qz = cv.RQDecomp3x3(rmat)

    x = angles[0] * 360
    y = angles[1] * 360
    z = angles[2] * 360

    return x,y,z
