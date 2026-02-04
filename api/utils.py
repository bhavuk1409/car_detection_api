import cv2
import numpy as np

def read_image(file_bytes: bytes):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def bbox_area(bbox):
    return (bbox["x2"] - bbox["x1"]) * (bbox["y2"] - bbox["y1"])

