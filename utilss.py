# import the required dependencies
import requests
import os

# Function to check internet connectivity
def internet_connect():
    try:
        # Sending a GET request to Google
        response = requests.get("http://www.google.com", timeout=5)
        # Checking if the response status is OK
        if response.status_code == 200:
            print("Internet connection is available.")
            return True
        else:
            print("Internet connection is not available.")
            return False
    except requests.ConnectionError:
        print("Internet connection is not available.")
        return False

# Function to find files with a specific extension in a folder
def find_files(folder_path, file_extension):
        try:
            # Initializing a list to store found files
            video_files = []
            # Walking through the directory tree
            for root, dirs, files in os.walk(folder_path):
                # Looping through files
                for file in files:
                    # Checking file extension
                    if file.endswith(file_extension):
                        # Adding the file path to the list
                        video_files.append(os.path.join(root, file))
        except Exception as exception:
            print("find_json_files method failed while Finding json location.", exception.args)
        finally:
            return video_files
        
# Function to find frames folders for multiple cameras in a root directory        
def find_frames_folders_multiple_cam(root_dir):
    try:
        # Initializing a dictionary to store frame folders
        frame_dict = {}
        # Looping through directories in the root directory
        for folder_name in os.listdir(root_dir):
            # Getting the complete folder path
            folder_path = os.path.join(root_dir, folder_name)
            # Getting the list of subfolders
            sub_folder_list = os.listdir(folder_path)
            # Looping through subfolders
            for folder in sub_folder_list:
                # Checking for a specific subfolder name
                if folder == "saved_folder":
                    # Getting the path of the 'saved_folder'
                    sub_folders_path = folder_path+"\\saved_folder"
                    # Checking if it's a directory
                    if os.path.isdir(sub_folders_path):
                        # Initializing a list to store subfolders
                        sub_folders = []
                        # Looping through subfolder names
                        for sub_folder_name in os.listdir(sub_folders_path):
                            # Complete subfolder path
                            sub_folder_path = os.path.join(sub_folders_path, sub_folder_name)
                            # if os.path.isfile(file_path) and file_name.endswith(file_extension):
                            # files.append(os.path.join(root_dir, folder_name, file_name))
                            # Adding subfolder path to the list
                            sub_folders.append(sub_folder_path)
                        # Adding subfolders to the dictionary
                        frame_dict[folder_name] = sub_folders
    except Exception as exception:
        print("find_frames_folders_multiple_cam method failed while Finding json location.", exception.args)
    finally:
        return frame_dict

# Function to list frames in a subfolder
def list_frames(subfolder):
    try:
        # Initializing a list to store frame paths
        frames = []
        # Looping through files in the subfolder
        for frame in os.listdir(subfolder):
            # Checking if it's a file
            if os.path.isfile(os.path.join(subfolder, frame)):
                # Adding frame path to the list
                frames.append(os.path.join(subfolder, frame))
    # Handling exceptions
    except Exception as exception:
        print("list_frames method failed while Finding json location.", exception.args)
    finally:
        # Returning the list of frame paths
        return frames
