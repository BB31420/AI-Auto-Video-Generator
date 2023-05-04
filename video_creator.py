import moviepy.editor as mpy
from moviepy.editor import concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from datetime import datetime

def create_video(images, voiceover_content, story, timestamp):
    # Save voiceover
    voiceover_filename = f"voiceover_{timestamp}.mp3"
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)

    # Generate image file names based on the timestamp and the index
    image_filenames = [f"image_{timestamp}_{idx}.png" for idx, _ in enumerate(images)]

    # Create video
    image_clips = [mpy.ImageClip(img).set_duration(5) for img in image_filenames] 
    video_clip = concatenate_videoclips(image_clips, method="compose")
    video_clip = video_clip.set_audio(mpy.AudioFileClip(voiceover_filename))

    video_filename = f"output_video_{timestamp}.mp4"  # The filename already includes a timestamp
    video_clip.write_videofile(video_filename, codec="libx264", fps=24)

    # Clean up files
    #for image_filename in image_filenames:
        #os.remove(image_filename)
    #os.remove(voiceover_filename)
