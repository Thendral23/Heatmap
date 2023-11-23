import urllib.request
import cv2 as cv
from constant import Constant
import re
import traceback

def internet_connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) 
        return True
    except:
        return False
    

def resize(frame):
    try:
        frame = cv.resize(frame, (Constant.IMAGE_HEIGHT,Constant.IMAGE_WIDTH))
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) 
        # frame = cv.normalize(frame, None, 0, 1.0, cv.NORM_MINMAX, dtype=cv.CV_32F)
        return frame
    except Exception as exception:
        print("resize failed", f"An error occurred on line {traceback.format_exc()}")


# def find_client_id(input_string):
#     try:
#         pattern = r'\*clt#(.*?)\*clt#'
#         client_id = re.findall(pattern, input_string)[0]
#         # for match in matches:
#         #     client_id = match[0]
#         #     cam_id = match[1]
#         #     print("client_id:", client_id)
#         #     print("cam_id:", cam_id)
#         return {"client_id":client_id}
#     except Exception as exception:
#         print("find_client_id failed", f"An error occurred on line {traceback.format_exc()}")


# def find_cam_id(input_string):
#     try:
#         pattern = r'\*cam#(.*?)\*cam#'
#         cam_id = re.findall(pattern, input_string)[0]
#         # for match in matches:
#         #     client_id = match[0]
#         #     cam_id = match[1]
#         #     print("client_id:", client_id)
#         #     print("cam_id:", cam_id)
#         return {"cam_id":cam_id}
#     except Exception as exception:
#         print("find_client_id failed", f"An error occurred on line {traceback.format_exc()}")
# '\*cam#(.*?)\*cam#'