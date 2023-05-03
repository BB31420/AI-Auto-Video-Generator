import requests
import os
import time

def generate_voiceover(story, save_file=False):
    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }
    data = {
        "text": story + "..Comment with your favorite fact...", 
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.6}
    }
    response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/GeEcOfn26FwkYBeN9dfZ", headers=headers, json=data)
    if response.status_code == 200:
        if save_file:
            with open("file.mp3", "wb") as f:
                f.write(response.content)
        return response.content
    else:
        print(f"Error while generating voiceover with status code {response.status_code}")
        return None

def save_voiceover(voiceover_content, timestamp):
    voiceover_filename = f"voiceover_{timestamp}.mp3"
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)
