from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

import sys
from models.video_cropper import save_img_range
from models.video_analyzer import analyze_video, encode_image

load_dotenv()
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Video Processing API!"

@app.route('/analyze_video', methods=['POST'])
def analyze_video_route():
    video_path = request.form.get('video_path')
    if not video_path:
        return jsonify({"error": "No video path provided"}), 400
    
    # Add your video analysis logic here
    # For example:
    # result = analyze_video(video_path)
    # return jsonify(result)

    return jsonify({"message": "Video analysis started"}), 200

if __name__ == "__main__":
    app.run(debug=True)
