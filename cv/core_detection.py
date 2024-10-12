import cv2
from roboflow import Roboflow
import os

#API Key Stuff
rf = Roboflow(api_key="jau6tLTx6Imi9ge2lwqf")
project = rf.workspace().project("shoplifting-cuzf8")
model = project.version(3).model

video_path = "video/shoplifting.mp4"

cap = cv2.VideoCapture(video_path)

#Don't mess with this
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

output_path = "updatedvideo.mp4"
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    temp_frame_path = f"temp_frame_{frame_count}.jpg"
    cv2.imwrite(temp_frame_path, frame)

    prediction = model.predict(temp_frame_path, confidence=40, overlap=30).json()

    os.remove(temp_frame_path)

    #Affects box size
    for obj in prediction['predictions']:
        x0 = int(obj['x'] - obj['width'] / 2)
        y0 = int(obj['y'] - obj['height'] / 2)
        x1 = int(obj['x'] + obj['width'] / 2)
        y1 = int(obj['y'] + obj['height'] / 2)
        label = obj['class']
        confidence = obj['confidence']

        cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
        #Affects text size
        cv2.putText(frame, f"{label}: {confidence:.2f}", (x0, y0 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    out.write(frame)

    frame_count += 1

cap.release()
out.release()

print(f"Processed video saved to {output_path}")
