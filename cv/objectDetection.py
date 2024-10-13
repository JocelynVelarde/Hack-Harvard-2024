import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification
import json

def classify_image(image_path):
    # Load the image
    image = Image.open(image_path)
    
    # Initialize the processor and model
    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')
    
    # Process the image and get model outputs
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    
    # Get the predicted class index
    predicted_class_idx = logits.argmax(-1).item()
    
    # Get the predicted class label
    predicted_class_label = model.config.id2label[predicted_class_idx]
    
    return predicted_class_label

# Example usage
if __name__ == "__main__":
    image_path = '../assets/lq_monster.png'
    result = classify_image(image_path)
    print(result)
