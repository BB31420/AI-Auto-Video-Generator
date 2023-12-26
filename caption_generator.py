import moviepy.editor as mpy
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

def extract_story_from_file(file_path):
    """Read the story from the given file path."""
    with open(file_path, 'r') as file:
        return file.read()

def create_caption_images(story, words_per_caption=5):
    """Convert the story into caption segments and generate images."""
    words = story.split()
    caption_segments = [' '.join(words[i:i + words_per_caption]) for i in range(0, len(words), words_per_caption)]
    
    caption_images = []
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)

    for segment in caption_segments:
        img = Image.new('RGBA', (1920, 100), (0, 0, 0, 100))
        d = ImageDraw.Draw(img)
        d.text((340, 10), segment, fill=(255, 255, 255, 255), font=font)
        caption_images.append(img)

    return caption_images

def add_captions_to_video(video_path, caption_images, output_path):
    """Overlay captions onto the video."""
    video_clip = mpy.VideoFileClip(video_path)
    total_duration = video_clip.duration
    num_captions = len(caption_images)
    avg_duration_per_caption = total_duration / num_captions
    
    caption_clips = []
    for idx, caption_img in enumerate(caption_images):
        start_time = idx * avg_duration_per_caption
        end_time = start_time + avg_duration_per_caption
        if end_time > total_duration:
            end_time = total_duration
        
        caption_img_array = np.array(caption_img)
        caption_clip = mpy.ImageClip(caption_img_array).set_duration(end_time - start_time).set_start(start_time).set_position(('left', 'bottom'))
        caption_clips.append(caption_clip)
    
    final_caption_clip = mpy.CompositeVideoClip(caption_clips, size=video_clip.size)
    final_video_clip = mpy.CompositeVideoClip([video_clip.set_duration(total_duration), final_caption_clip.set_duration(total_duration)])
    
    final_video_clip.write_videofile(output_path, codec="libx264", fps=24)
