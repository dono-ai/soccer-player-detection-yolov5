""" ---------------------- Create Yolo format dataset ----------------------"""
import shutil, os, cv2, glob, json
import numpy as np
import matplotlib.pyplot as plt
from pprintpp import pprint

input_root = "../data"
input_subdir = "football"

output_root = "../datasets"

dataset_types = ["train", "test"]



def create_yolo_dataset(input_root: str, input_subdir: str, output_root: str, type:str ="train"):
    
    # if os.path.isdir(output_root):
    #     shutil.rmtree(output_root)
    
    os.makedirs(f"{output_root}/images/{type}")
    os.makedirs(f"{output_root}/labels/{type}")
    
    input_data_path = f"{input_root}/{input_subdir}/{type}"

    vid_paths = [file.replace(".mp4", "") for file in glob.glob(f"{input_data_path}/*/*.mp4")]
    json_paths = [file.replace(".json", "") for file in glob.glob(f"{input_data_path}/*/*.json")]
    valid_paths = list(set(vid_paths) & set(json_paths))

    file_id = 0
    for path in valid_paths:
        with open(f"{path}.json", "r") as f:
            json_data = json.load(f)
        annotations = json_data["annotations"]
        frame_width = json_data["images"][0]["width"]
        frame_height = json_data["images"][0]["height"]
        cap = cv2.VideoCapture(f"{path}.mp4")

        frame_id = 1
        while cap.isOpened():
            flag, frame = cap.read()
            if not flag:
                print(f"Finished or error reading a video's frame: {path}.mp4")
                break
            
            cv2.imwrite(f"{output_root}/images/{type}/{file_id}.jpg", frame)
            
            with open(f"{output_root}/labels/{type}/{file_id}.txt", "w") as f:
                for anno in annotations:
                    if anno["image_id"] == frame_id and anno["category_id"] == 4:
                        class_id = 0
                        xmin, ymin, object_width, object_height = anno["bbox"]
                        xcenter = (int(xmin + object_width/2))/frame_width # conver xmin to xcenter + normalize xcenter
                        ycenter = (int(ymin + object_height/2))/frame_height # conver xmin to ycenter + normalize ycenter
                        object_width /= frame_width
                        object_height /= frame_height
                        f.write(f"{class_id:06f} {xcenter:06f} {ycenter:06f} {object_width:06f} {object_height:06f} \n")
            
            frame_id += 1
            file_id += 1
        cap.release()         
    print(f"\n************************ finished creating {type} ************************")
    
# file names   0 - 1499    1500 - 2999     3000 - 4499
# frames       1 - 1500    1 - 1500        1 - 1500


create_yolo_dataset(input_root, input_subdir ,output_root, "train")
create_yolo_dataset(input_root, input_subdir ,output_root, "test")
