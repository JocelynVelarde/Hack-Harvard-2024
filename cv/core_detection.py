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
        self.prediction_data = []  #Internal storage for predictions during processing

    def process_video(self, video_path, output_video_path, confidence_threshold=40, overlap_threshold=30):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        #DO NOT EDIT THESE!!
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            temp_frame_path = f"temp_frame_{frame_count}.jpg"
            cv2.imwrite(temp_frame_path, frame)

            #Make prediction and store it internally
            prediction = self.model.predict(temp_frame_path, confidence=confidence_threshold, overlap=overlap_threshold).json()

            #Process the prediction to classify into 3 levels
            processed_predictions = self.classify_predictions(prediction['predictions'])

            self.prediction_data.append({"frame": frame_count, "predictions": processed_predictions})

            frame = self.draw_predictions_on_frame(frame, processed_predictions)

            out.write(frame)

            os.remove(temp_frame_path)
            frame_count += 1

        cap.release()
        out.release()
        print(f"Video processed and saved to {output_video_path}. {frame_count} frames analyzed.")

    def classify_predictions(self, predictions):
        processed_predictions = []
        for obj in predictions:
            confidence = obj['confidence']
            label = obj['class']
            
            #Some simple logic to determine behavior (this isn't neccessarily a good metric though, if you want to know why ask me I'm too lazy to type it here)
            if confidence > 0.6:
                level = 'normal'
            elif 0.4 <= confidence < 0.6:
                level = 'damgerous'
            else:
                level = 'suspicious'

            processed_predictions.append({
                "x": obj['x'],
                "y": obj['y'],
                "width": obj['width'],
                "height": obj['height'],
                "confidence": confidence,
                "class": label,
                "level": level
            })

        return processed_predictions

    def draw_predictions_on_frame(self, frame, predictions):
        for obj in predictions:
            #Calculates the box bounds/coordinates
            x0 = int(obj['x'] - obj['width'] / 2)
            y0 = int(obj['y'] - obj['height'] / 2)
            x1 = int(obj['x'] + obj['width'] / 2)
            y1 = int(obj['y'] + obj['height'] / 2)

            # Set the label text with class and level (normal, suspicious, dangerous)
            label = f"{obj['class']}: {obj['level']} ({obj['confidence']:.2f})"

            #Boxes
            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
            
            #Text
            cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        return frame

    def get_predictions(self, formatted=False):
        if formatted:
            return json.dumps(self.prediction_data, indent=4)
        return self.prediction_data