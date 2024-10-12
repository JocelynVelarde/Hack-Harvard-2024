import cv2
from roboflow import Roboflow
import os
import json
from collections import deque

class ShopliftingDetector:
    def __init__(self, api_key_file, project_name, version_num):
        with open(api_key_file, 'r') as f:
            service_key = json.load(f)
        
        rf = Roboflow(api_key=service_key["api_key"])
        project = rf.workspace().project(project_name)
        self.model = project.version(version_num).model
        self.prediction_data = []  #Internal storage for predictions during processing
        self.frame_buffer = deque(maxlen=120)
        self.active_event = False
        self.event_frame_count = 0
        self.event_clip_writer = None

    def process_video(self, video_path, output_video_path, confidence_threshold=30, overlap_threshold=30):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        #Do not change this!!!
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

        #Gets 2 seconds worth of frames
        suspicious_frames = deque(maxlen=int(fps * 2))
        post_event_frames = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            temp_frame_path = f"temp_frame_{frame_count}.jpg"
            cv2.imwrite(temp_frame_path, frame)

            #Makes a prediction and then stores it internally here
            prediction = self.model.predict(temp_frame_path, confidence=confidence_threshold, overlap=overlap_threshold).json()

            #Put it into 1 of the 3 categories
            processed_predictions = self.classify_predictions(prediction['predictions'])

            self.prediction_data.append({"frame": frame_count, "predictions": processed_predictions})

            #Draws the labels + boxes
            frame = self.draw_predictions_on_frame(frame, processed_predictions)

            self.frame_buffer.append(frame)

            #Checks if there's a sus ;) or dangerous event
            is_event = self.detect_event(processed_predictions)

            #Basically, if it is an event, create a new clip
            if is_event:
                #Capture 2 seconds before and after the event
                if not self.active_event:
                    print(f"Event started at frame {frame_count}")
                    #Create a video for the event
                    self.start_event_clip(frame_width, frame_height, fps, frame_count)
                    self.active_event = True
                    post_event_frames = 0

                #Get the frames 2 seconds before the event
                while self.frame_buffer:
                    buffered_frame = self.frame_buffer.popleft()
                    self.event_clip_writer.write(buffered_frame)

                #Get the current frame and apply it to the clip
                self.event_clip_writer.write(frame)

                post_event_frames = 0
            else:
                if self.active_event:
                    post_event_frames += 1

                    #Get the frames 2 seconds after the clip
                    self.event_clip_writer.write(frame)

                    #End the clip if it has beem 2 seconds after the event occured
                    if post_event_frames >= fps * 2:
                        print(f"Event ended at frame {frame_count}")
                        self.stop_event_clip()
                        self.active_event = False

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
            
            #Simple logic for determining if it's normal, sus ;), or dangerous (this is not an accurate way of doing this, but will work for this project. if you have questions come ask me and i'll explain it i just don't want to type out the explanation right now)
            if confidence > 0.6:
                level = 'normal'
            elif 0.4 <= confidence < 0.6:
                level = 'dangerous'
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

    def detect_event(self, predictions):
        for obj in predictions:
            if obj['level'] in ['suspicious', 'dangerous']:
                return True
        return False

    #Creates a new clip
    def start_event_clip(self, frame_width, frame_height, fps, frame_count):
        event_clip_name = f"event_clip_{frame_count}.mp4"
        self.event_clip_writer = cv2.VideoWriter(event_clip_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
        print(f"Recording event clip: {event_clip_name}")

    #Obviously ends the clip
    def stop_event_clip(self):
        if self.event_clip_writer:
            self.event_clip_writer.release()
            print("Event clip saved.")

    def draw_predictions_on_frame(self, frame, predictions):
        for obj in predictions:
            #Calculates the box's bounds/coordiantes
            x0 = int(obj['x'] - obj['width'] / 2)
            y0 = int(obj['y'] - obj['height'] / 2)
            x1 = int(obj['x'] + obj['width'] / 2)
            y1 = int(obj['y'] + obj['height'] / 2)

            #Label text template
            label = f"{obj['class']}: {obj['level']} ({obj['confidence']:.2f})"

            #Draws box
            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
            
            #Draws text
            cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return frame

    def get_predictions(self, formatted=False):
        if formatted:
            return json.dumps(self.prediction_data, indent=4)
        return self.prediction_data