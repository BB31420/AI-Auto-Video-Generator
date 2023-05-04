import time
from story_generator import generate_story, save_story_with_image_prompts
from keyword_identifier import extract_image_prompts
from image_generator import generate_images, save_images
from voiceover_generator import generate_voiceover, save_voiceover
from video_creator import create_video

def main():
    timestamp = int(time.time())

    # Get user input
    story_prompt = input("Enter a story prompt: ")

    story, final_story_prompt = generate_story(story_prompt)  # Update the assignment to get the final_story_prompt
    print("Story generated successfully.")

    # Generate image Prompts
    image_prompts = extract_image_prompts(story)
    print("Image prompts extracted.")
    
    # Save the story and image prompts together
    save_story_with_image_prompts(story, final_story_prompt, image_prompts)  # Use final_story_prompt instead of story_prompt

    # Generate images
    images = generate_images(image_prompts)
    print("Images generated successfully.")
    save_images(images, timestamp)

    # Generate the voiceover
    voiceover = generate_voiceover(story)
    if voiceover:
        print("Voiceover generated successfully.")
        save_voiceover(voiceover, timestamp)
    else:
        print("Voiceover generation failed.")

    # Create the video
    create_video(images, voiceover, story, timestamp)
    print("Video created successfully.")

if __name__ == "__main__":
    main()
