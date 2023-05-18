import cv2 as cv
import numpy as np

image = np.zeros((400,400,3), np.uint8)

def draw_lines(arr1, arr2, offsetX = 0, offsetY = 200, scale = 100):
    offsetArr = np.array([offsetX,offsetY])
    cv.line(image, offsetArr, arr1 + offsetArr, color=(0,0,255))
    cv.line(image, offsetArr, arr2 + offsetArr, color=(0,255,0))

def reset_image():
    global image
    image = np.zeros((500,900,3), np.uint8)
    