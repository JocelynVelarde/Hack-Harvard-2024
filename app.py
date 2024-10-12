from flask import Flask
import os
from dotenv import load_dotenv

import sys
import os
from models.video_cropper import save_img_range
from models.video_analyzer import analyze_video, encode_image

load_dotenv()
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Video Processing API!"

@app.route('/analyze_video', methods=['POST'])
def analyze_video_route():
    video_path = flask.request.form.get('video_path')
    if not video_path:
        return flask.jsonify({"error": "No video path provided"}), 400
    
    try:
        analysis_result = analyze_video(video_path)
        return flask.jsonify({"result": analysis_result}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

@app.route('/save_img_range', methods=['POST'])
def save_img_range_route():
    video_path = flask.request.form.get('video_path')
    start_time = flask.request.form.get('start_time')
    end_time = flask.request.form.get('end_time')
    
    if not video_path or not start_time or not end_time:
        return flask.jsonify({"error": "Missing parameters"}), 400
    
    try:
        save_img_range(video_path, start_time, end_time)
        return flask.jsonify({"message": "Images saved successfully"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

@app.route('/encode_image', methods=['POST'])
def encode_image_route():
    image_path = flask.request.form.get('image_path')
    if not image_path:
        return flask.jsonify({"error": "No image path provided"}), 400
    
    try:
        encoded_image = encode_image(image_path)
        return flask.jsonify({"encoded_image": encoded_image}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
