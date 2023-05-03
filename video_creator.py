import moviepy.editor as mpy
from moviepy.editor import concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from datetime import datetime

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

def create_video(images, voiceover_content, story, timestamp):
    # Save voiceover
    voiceover_filename = f"voiceover_{timestamp}.mp3"
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)

    # Generate image file names based on the timestamp and the index
    image_filenames = [f"image_{timestamp}_{idx}.png" for idx, _ in enumerate(images)]

    # Add text to each image
    # Note: This assumes that 'story' is a list of strings, where each string is the text for one image.
    # You might need to adjust this part based on how your 'story' variable is structured.
    #for idx, image_filename in enumerate(image_filenames):
        #add_text_to_image(image_filename, story[idx])

    # Create video
    image_clips = [mpy.ImageClip(img).set_duration(4) for img in image_filenames] 
    video_clip = concatenate_videoclips(image_clips, method="compose")
    video_clip = video_clip.set_audio(mpy.AudioFileClip(voiceover_filename))

    video_filename = f"output_video_{timestamp}.mp4"  # The filename already includes a timestamp
    video_clip.write_videofile(video_filename, codec="libx264", fps=24)

    # Clean up files
    #for image_filename in image_filenames:
        #os.remove(image_filename)
    #os.remove(voiceover_filename)
