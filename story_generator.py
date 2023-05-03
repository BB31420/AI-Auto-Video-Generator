import openai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

def generate_story(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 400,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    story = response.choices[0].text.strip()
    print(story)
    return story

def save_story(story, prompt):
    with open(f"story_{timestamp}.txt", "w") as f:
        f.write(prompt + "\n" + story)
