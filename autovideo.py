import openai
import requests
import json
import moviepy.editor as mpy
from moviepy.editor import concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import time
import textwrap

load_dotenv()

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Step 1: Get user input
story_prompt = input("Enter a story prompt: ")

# Step 2: Use ChatGPT API to generate story
def generate_story(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.7,
    )
    story = response.choices[0].text.strip()
    return story

# Save story to a file
def save_story(story):
    with open(f"story_{timestamp}.txt", "w") as f:
        f.write(story)

# Step 3: Extract key information for DALL-E
def extract_image_prompts(story, num_prompts=4):
    tokens = word_tokenize(story.lower())
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    common_keywords = [item[0] for item in Counter(filtered_tokens).most_common(num_prompts)]

    image_prompts = [f"{keyword} illustration" for keyword in common_keywords]
    return image_prompts

# Step 4: Use DALL-E API to generate images
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

    return images

# Save images to files
def save_images(images):
    for idx, image_url in enumerate(images):
        download_image(image_url, f"image_{timestamp}_{idx}.png")


# Step 5: Use Elvenlabs API to generate voiceover
def generate_voiceover(story, save_file=False):
    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }
    data = {
        "text": story, 
        "voice_settings": {"stability": 0.5, "similarity_boost": 0}
    }
    response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/GeEcOfn26FwkYBeN9dfZ", headers=headers, json=data)
        # Voices: 21m00Tcm4TlvDq8ikWAM  yoZ06aMxZJJ28mfd3POQ  AZnzlk1XvdvUeBnXmlld
    if response.status_code == 200:
        if save_file:
            with open("file.mp3", "wb") as f:
                f.write(response.content)
        return response.content
    else:
        print(f"Error while generating voiceover with status code {response.status_code}")
        return None

# Save voiceover to a file
def save_voiceover(voiceover_content, timestamp):
    voiceover_filename = f"voiceover_{timestamp}.mp3"
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)


# Step 6: Combine images, voiceover, and text into a video
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)

def add_text_to_image(image_path, text):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Gabriola.ttf", size=40)  # Change the font size here
    text_color = (64, 64, 64)  # Black color
    bg_color = (255, 204, 0, 120)  # White semi-transparent background color
    padding = 50
    max_width = image.width - 2 * padding

    # Calculate the average character width
    avg_char_width = sum(font.getsize(char)[0] for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") / 52

    # Calculate the maximum number of characters per line
    max_chars_per_line = int(max_width / avg_char_width)

    # Wrap the text
    wrapped_text = textwrap.wrap(text, width=max_chars_per_line)

    # Calculate the height of the wrapped text
    text_height = len(wrapped_text) * font.getsize(wrapped_text[0])[1]

    # Calculate the y-coordinate to position the text at the bottom
    y_position = image.height - text_height - padding

    # Draw a background rectangle behind the text
    bg_rect_height = text_height + 2 * padding
    bg_rect_y_position = y_position - padding
    draw.rectangle([(padding, bg_rect_y_position), (image.width - padding, bg_rect_y_position + bg_rect_height)], fill=bg_color)

    # Draw each line of the wrapped text
    for idx, line in enumerate(wrapped_text):
        line_y_position = y_position + idx * font.getsize(line)[1]
        draw.text((padding, line_y_position), line, font=font, fill=text_color)

    image.save(image_path)



def create_video(images, voiceover_content, story):
    # Save voiceover
    voiceover_filename = "voiceover.mp3"
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)

    # Download images and add text
    image_filenames = []
    for idx, image_url in enumerate(images):
        image_filename = f"image_{idx}.png"
        download_image(image_url, image_filename)
        add_text_to_image(image_filename, story)
        image_filenames.append(image_filename)

    # Create video
    image_clips = [mpy.ImageClip(img).set_duration(2) for img in image_filenames]
    video_clip = concatenate_videoclips(image_clips, method="compose")
    video_clip = video_clip.set_audio(mpy.AudioFileClip(voiceover_filename))
    #video_clip.write_videofile("output_video.mp4", codec="libx264", fps=24)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Get the current timestamp
    video_filename = f"output_video_{timestamp}.mp4"  # Add timestamp to filename
    video_clip.write_videofile(video_filename, codec="libx264", fps=24)

    # Clean up files
    for image_filename in image_filenames:
        os.remove(image_filename)
    os.remove(voiceover_filename)
# ...

nltk.download("punkt")
nltk.download("stopwords")

story = generate_story(story_prompt)
print("Story generated successfully.")
save_story(story)

image_prompts = extract_image_prompts(story)
print("Image prompts extracted.")

images = generate_images(image_prompts)
print("Images generated successfully.")
save_images(images)

# Generate the voiceover
voiceover = generate_voiceover(story)
if voiceover:
    print("Voiceover generated successfully.")
    timestamp = int(time.time())  # Get the current timestamp
    save_voiceover(voiceover, timestamp)  # Pass the timestamp as the second argument
else:
    print("Voiceover generation failed.")

create_video(images, voiceover, story)
print("Video created successfully.")
