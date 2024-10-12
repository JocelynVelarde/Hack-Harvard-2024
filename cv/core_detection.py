import cv2
from roboflow import Roboflow
import os
import json

class ShopliftingDetector:
    def __init__(self, api_key_file, project_name, version_num):
        with open(api_key_file, 'r') as f:
            service_key = json.load(f)
        
        rf = Roboflow(api_key=service_key["api_key"])
        project = rf.workspace().project(project_name)
        self.model = project.version(version_num).model
        self.prediction_data = []

    def process_video(self, video_path, confidence_threshold=40, overlap_threshold=30):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            temp_frame_path = f"temp_frame_{frame_count}.jpg"
            cv2.imwrite(temp_frame_path, frame)

            prediction = self.model.predict(temp_frame_path, confidence=confidence_threshold, overlap=overlap_threshold).json()

            self.prediction_data.append({"frame": frame_count, "predictions": prediction['predictions']})

            os.remove(temp_frame_path)
            frame_count += 1

        cap.release()
        print(f"Video processed. {frame_count} frames analyzed.")

    def get_predictions(self, formatted=False):
        if formatted:
            return json.dumps(self.prediction_data, indent=4)
        return self.prediction_data