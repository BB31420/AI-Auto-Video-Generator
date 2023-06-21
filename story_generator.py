import openai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

def generate_story(prompt):
    while True:
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
        print("Generated Story:")
        print(story)
        
        # Ask the user whether they want to proceed, generate another story, or write their own story
        user_input = input("\nDo you want to proceed with this? (y/n/custom): ")
        if user_input.lower() == "yes":
            return story, prompt  # Return both the story and the prompt used
        elif user_input.lower() == "no":
            prompt = input("\nEnter a new prompt: ")
        elif user_input.lower() == "custom":
            custom_story = input("Write your custom story: ")
            return custom_story, prompt  # Return the custom story and the original prompt
        else:
            print("Invalid input. Please enter 'y' to proceed with the current story, 'n' to generate another story, or 'custom' to write your own story.")

def save_story_with_image_prompts(story, prompt, image_prompts):
    with open(f"story_{timestamp}.txt", "w") as f:
        f.write(prompt + "\n" + story + "\n\nImage Prompts:\n")
        for idx, image_prompt in enumerate(image_prompts, start=1):
            f.write(f"{idx}: {image_prompt}\n")
