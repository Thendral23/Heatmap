# Import the required dependencies
from save_data_points import SaveDataPoints
import cv2
from constant import Constant
import time
import os
from datetime import datetime
import logging
import shutil
from utilss import *

# Setting up log file
log_file = Constant.LOG_FILE_SAVE_DATA_POINTS
if os.path.exists(log_file):
    # Clearing the log file if it exists
    open(log_file, 'w').close()

# Configuring logging settings
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S')


# Defining the main function to execute the process
def main():
    # Running the process continuously
    while True:
        # Creating an instance of SaveDataPoints class
        savedatapoints_ = SaveDataPoints()
        # Checking if there are no video files
        if len(savedatapoints_.source_dict) == 0:
            print("There is no video file")
            time.sleep(Constant.SAVE_VIDEO_DURATION * 60 + 40)
            # Continuing to the next iteration
            continue
        else:
            # Looping through cameras and subfolders
            for (cam, subfolder_list) in savedatapoints_.source_dict.items():
                # Checking if subfolder list is empty
                if len(subfolder_list) == 0:
                    # shutil.rmtree(sub_folder)
                    continue
                # Looping through subfolders
                for sub_folder in subfolder_list:
                    # Getting a list of frames in the subfolder
                    frames_list = list_frames(sub_folder)
                    # Checking if frames list is empty
                    if len(frames_list) == 0:
                        # Removing the empty subfolder
                        shutil.rmtree(sub_folder)
                        break
                    # Initializing frame for processing
                    savedatapoints_.initialize_frame(cam, frames_list[0])
                    break

            for (cam, subfolder_list) in savedatapoints_.source_dict.items():
                for sub_folder in subfolder_list:
                    # Setting start time for data processing
                    savedatapoints_.start_time = datetime.now()
                    while True:
                        # Reading frames and processing data
                        savedatapoints_.read_frames(sub_folder, Constant.SCALE_FACTOR)
                        # Saving data points to JSON
                        savedatapoints_.save_datapoints_to_json(cam, sub_folder)
                        break
                    # Updating the save timestamp
                    Constant.SAVE_TIMESTAMP = datetime.now()

                    try:
                        # Removing the processed subfolder and its contents
                        shutil.rmtree(sub_folder)
                        print(f"The folder {sub_folder} and its contents have been successfully removed.")
                    except OSError as e:
                        print(f"Error: {sub_folder} : {e.strerror}")


# Executing the main function if this script is directly run       
if __name__ == "__main__":
    main()
    