import os
from datetime import datetime

class Constant:
    SERVER_HOST = '127.0.0.1'
    ROOT_DIR = os.getcwd() + "\\"
    PATH_SAVE_FRAMES = ROOT_DIR + "input_folder\\saved_frames_at"
    TIME_TO_WAIT = 6 # in seconds
    TIME_TO_WAIT_TO_SEND_FRAMES = 3
    SOURCE_URLS = ["rtsp://tapoc1:cv1234@192.168.0.128:554/stream1"]#, "rtsp://tapoc1:cv1234@192.168.0.128:554/stream1", "rtsp://tapoc1:cv1234@192.168.0.128:554/stream1"]
    SERVER_PORT =12345
    IMAGE_HEIGHT = 640
    IMAGE_WIDTH = 280
    CLIENT_ID = "Elan Thendral--"
    CLIENT_ID_INDEXING_END = 15
    CAM_ID_INDEXING_START = 15
    CAM_ID_INDEXING_END = 20
    FRAME_DATA_DECODE_INDEXING_START = 25
    BYTE_LENGTH = 4096
    current_dir = None
    

    ## Save data points constants ##
    SAVE_TIMESTAMP = datetime.now()
    FRAME_COUNT = 0
    FRAME_TO_CALCULATE = 3
    SCALE_FACTOR = 0.25
    ROOT_DIR = os.getcwd() + "\\"
    # CLIENT_ID_ = "\\Elan Thendral--"
    SAVE_VIDEO = ROOT_DIR + "input_folder\\saved_frames_at"
    VIDEO_EXTENSION = '.mp4'
    SAVE_JSON = ROOT_DIR + f"json_folder\\"
    JSON_EXTENSION = '.json'
    RTSP_SOURCE = "rtsp://192.168.0.124:8080/h264_ulaw.sdp"
    SAVE_VIDEO_DURATION = 3  # minutes
    SOURCE = ROOT_DIR + "input_folder\\"
    WRITE_LOCATION = ROOT_DIR + "output_folder\\"
    DEL_VIDEO_LOCATION = ROOT_DIR + "input_folder\\saved_video_at"
    START_TIME_TO_UPDATE_HM = 10
    END_TIME_TO_UPDATE_HM = 17
    TARGET_DATE = '20231121'
    TARGET_CAM = 'Cam_1'
    INITIAL_FRAME_FOLDER = ROOT_DIR + "input_folder\\frame_to_merge_with_heatmap\\"
    LOG_FILE = "log.txt"
    RTSP_SOURCE_LIST = [
        "rtsp://tapoc1:cv1234@192.168.1.3:554/stream1",
        "rtsp://tapoc1:cv1234@192.168.1.3:554/stream1"
    ]
    LOG_FILE_SAVE_DATA_POINTS = ROOT_DIR + "Save_data_points_log.log"
    LOG_FILE_SAVE_VIDEOS = ROOT_DIR + "Save_videos_log.log"
    AVG_FRMAE_COUNT = 1200
