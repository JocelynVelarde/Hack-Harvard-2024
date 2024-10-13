import requests
import base64
import streamlit as st
from PIL import Image
from models.video_cropper import save_img_range
from io import BytesIO
import logging
import os

def encode_image(image):
    if isinstance(image, str):
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    elif isinstance(image, Image.Image): 
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    else:
        raise TypeError("Expected str or PIL.Image.Image")
    
def cloudflare_analysis(video_name : str, video_ext : str = 'mp4') -> str:
    img_count = save_img_range(f'{video_name}.{video_ext}', 0, 4, 0.75, '.', f'{video_name}_image')
    logging.info(f"Image count: {img_count}")

    if img_count:
        images = []
        for i in range(1, img_count + 1):
            images.append(Image.open(f'{video_name}_image_{i}.jpg'))
        
        logging.info(f"Images: {images}")

        if not isinstance(images, list):
            images = [images]

        inputs = [
            {
                "image": encode_image(image=image), 
                "max_tokens": 512, 
                "temperature": 0.7, 
                "prompt": "Analyze the content of the image.",  
                "raw": False 
            } for image in images
        ]

        # Getting the base64 string

        account_id = st.secrets["CLOUDFLARE"]["ACCOUNT_ID"]

        API_BASE_URL = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/'
        headers = {
            "Authorization": f"Bearer {st.secrets['CLOUDFLARE']['API_KEY']}"
        }

        def run(model, inputs):
            response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=inputs)
            return response.json()

        output = run("@cf/unum/uform-gen2-qwen-500m", inputs)

        logging.info(f"Output: {output}")

        for i in range(1, img_count + 1):
            os.remove(f'{video_name}_image_{i}.jpg')

        return output

def openai_analsis(video_name : str, video_ext : str = 'mp4', objectContext: str = '', facialContext: str='') -> str:
    img_count = save_img_range(f'{video_name}.{video_ext}', 0, 4, 0.75, '.', f'{video_name}_image')

    logging.info(f"Image count: {img_count}")

    if img_count:
        images = []
        for i in range(1, img_count + 1):
            images.append(Image.open(f'{video_name}_image_{i}.jpg'))

        logging.info(f"Images: {images}")

        if not isinstance(images, list):
            images = [images]
        
        encoded_images = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{encode_image(image)}"
                }
            } for image in images
        ]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.secrets["OPENAI"]['OPENAI_API_KEY']}"
        }

        messages = [
            {
                "role": "system",
                "content": "You are an assistant that provides event descriptiosn for an automated theft detection system for a store. You will analyze the provided images which are part of a video, try to see if there is any suspicious activity, like shoplifting, and provide a description of the event."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Based off the provided video and information from different part of the system, can you tell if there are any suspicious or dangerous activities happening in regards to shoplifting? 
                                {objectContext} is the context of the objects in the video and {facialContext} is the context of the faces in the video. Please include this information in your analysis if any. If there exists any of the contexts then just skip over and dont address it."  

                    }
                ] + encoded_images
            }
        ]

        # Prepare the payload
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "max_tokens": 350
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()

            logging.info(f"Response data: {response_data}")

            if 'choices' in response_data and response_data['choices']:
                output_message = response_data['choices'][0]['message']['content']

                logging.info(f"Output message: {output_message}")
                
                for i in range(1, img_count + 1):
                    os.remove(f'{video_name}_image_{i}.jpg')

                return output_message
            else:
                for i in range(1, img_count + 1):
                    os.remove(f'{video_name}_image_{i}.jpg')
                return "No response or incomplete response from API."

        except requests.exceptions.RequestException as e:
            for i in range(1, img_count + 1):
                    os.remove(f'{video_name}_image_{i}.jpg')
            return f"API request failed: {e}"
    else :
        return "No images found for this video name"

def analyze_video(video_name : str, video_ext : str = 'mp4') -> str:
    try :
        res = cloudflare_analysis(video_name, video_ext)

        if res['errors'][0]['code'] == 5006:
            raise Exception("Cloudflare API error occured")
    except Exception as e:
        logging.error(f"Error in cloudflare analysis: {e}")
        try:
            return openai_analsis(video_name, video_ext)
        except Exception as e:
            logging.error(f"Error in openai analysis: {e}")
            return "Error in both analysis"


def chat_prompt(result, user_prompt, api_key):
    # Combine previous analysis results into a single context string
    context = "\n".join([f"{key}: {value}" for key, value in result.items()])

    # Construct the new message with context and user prompt
    messages = [
        {
            "role": "system",
            "content": context
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Message after the user prompt
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "max_tokens": 250
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    # Extract the output message
    output_message = response_data['choices'][0]['message']['content']
    return output_message