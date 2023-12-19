import openai
import os
import requests
from datetime import datetime
import time

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_images(image_prompts):
    images = []

    for prompt in image_prompts:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )

        if response.data:
            image_url = response.data[0].url
            images.append(image_url)
        else:
            print(f"Error generating image for prompt '{prompt}'")
            return []
        time.sleep(12)    
    return images

def save_images(images, timestamp):
    
    for idx, image_url in enumerate(images):
        download_image(image_url, f"image_{timestamp}_{idx}.png")

def download_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
