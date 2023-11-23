# Import the required dependencies
import cv2
from model import Model
import json
from constant import Constant
from utilss import find_frames_folders_multiple_cam, list_frames
import os
import logging
import shutil

# Setting up log file
log_file = Constant.LOG_FILE_SAVE_DATA_POINTS

# Clearing log file if it exists
if os.path.exists(log_file):
    open(log_file, 'w').close()

# Configuring logging settings
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S')

# Defining a class to handle data point extraction
class SaveDataPoints(Model):

    def __init__(self):
        # Initializing parent class
        super().__init__()
        try:
            self.data_points = []  # Initializing data points list
            self.source_dict = self.find_frames_folders()   # Finding frame folders
            # Handling case where no frame folders are found
            if len(self.source_dict) == 0:
                pass  
        except Exception as exception:
            print("Constructor method failed while loading source", exception.args)

    # Finding frame folders for multiple cameras
    def find_frames_folders(self):
        video_file_dict = find_frames_folders_multiple_cam(Constant.SAVE_VIDEO+"\\"+Constant.CLIENT_ID)
        return video_file_dict
    
    # Initializing a frame for merging with a heatmap
    def initialize_frame(self, cam, frame):
        try:
            path = Constant.INITIAL_FRAME_FOLDER+f"{Constant.CLIENT_ID}\\" + f'{cam}'
            if os.path.exists(path):
                # Removing existing folder and its contents
                shutil.rmtree(path)  
                os.makedirs(path, exist_ok=True)
                # Copying the frame to the initialized path
                shutil.copy(frame, path)  
            else:
                os.makedirs(path, exist_ok=True)
                shutil.copy(frame, path)
            logging.info(f"Frame initialized succesfully to merge with heatmap in {cam}")
            print("Frame initialized succesfully to merge with heatmap.")
            print("------------------------------------------------------")
        except Exception as exception:
            print("initialize_frame method failed while initializing the frame.", exception.args)

    # Reading frames from a subfolder with a specified scale factor
    def read_frames(self, subfolder, scale_factor):
        try:
            # Getting a list of frames in the subfolder
            frames_list = list_frames(subfolder)   
            for frame_path in frames_list:
                # Reading the frame
                frame = cv2.imread(frame_path)    
                if frame is None:
                     # Returning data points if frame is None
                    return self.data_points     
                            
                if frame is not None:
                    # Perform object detection
                    # Running the model for object detection
                        results = self.model(frame)  
                        # Extracting detections from the results obtained after object detection
                        detections = results.pandas().xyxy[0]   
                        # Iterating through each detected object 
                        for _, detection in detections.iterrows():
                            # Checking if the detected object is a 'person'
                            if detection['name'] == 'person':
                                # Extracting coordinates (x, y, width, height) of the detected 'person'
                                x, y, w, h = int(detection['xmin']), int(detection['ymin']), int(
                                    detection['xmax'] - detection['xmin']), int(detection['ymax'] - detection['ymin'])
                                # Calculating new coordinates and dimensions based on a scale factor
                                delta_x, delta_y, new_width, new_height = self.roi(x, y, w, h, scale_factor)
                                # Creating data points for the detected 'person'
                                data_point = {
                                    'x': delta_x,
                                    'y': delta_y,
                                    'width': new_width,
                                    'height': new_height
                                }
                                # Appending data points
                                self.data_points.append(data_point)  
                # Removing the processed frame   
                os.remove(frame_path)         
        except Exception as exception:
            print("read_frames method failed while reading the frame", exception.args)

    # Calculating region of interest based on coordinates and scale factor
    def roi(self, x, y, w, h, scale_factor):
        try:
            # Calculating the new width of the bounding box based on the given scale factor
            new_width = int(w * scale_factor)
            # Calculating the new height of the bounding box based on the given scale factor
            new_height = int(h * scale_factor)
            # Calculating the new x-coordinate to adjust the bounding box based on the scale factor
            delta_x = x + int((w - new_width) / 2)
            # Calculating the new y-coordinate to adjust the bounding box based on the scale factor
            delta_y = y + int((h - new_height) / 2)
            # Returning the adjusted coordinates and dimensions of the bounding box
            return delta_x, delta_y, new_width, new_height
        except Exception as exception:
            print("roi method failed while calculating region of interest", exception.args)
    
    # Removing a video file
    def remove_video_file(self, file_path):
        try:
            os.remove(file_path)
            print("Video is sucessfuly removed from directory after data points collect.......")
            print("----------------------------------------------------------------------------")
            logging.info("Video is sucessfully removed from directory after data points collect.......")
        except Exception as exception:
            print("Failed to remove video file:", exception.args)
            logging.info("Failed to remove video file.")

    # Saving data points to a JSON file
    def save_datapoints_to_json(self, cam, source):
        try:
            if not os.path.exists(Constant.SAVE_JSON + f"\\{Constant.CLIENT_ID}\\{cam}"):
                os.mkdir(Constant.SAVE_JSON + f"{cam}")
            filename = os.path.basename(source)
            file_path = Constant.SAVE_JSON + f"{Constant.CLIENT_ID}\\{cam}\\data_points___{filename}.json"
            # Writing data points to a JSON file
            with open(file_path, 'w') as file:
                json.dump(self.data_points, file)
            print("Json file is sucessfully saved with data points......")
            print("---------------------------------------------------------------------------")
            logging.info("Json file is sucessfully saved with data points......")
            # Clearing data points after saving to file
            self.data_points.clear()
        except Exception as exception:
            print("Save data points to JSON method failed while saving data points:", exception.args)
            logging.info("Save data points to JSON method failed while saving data points.")
