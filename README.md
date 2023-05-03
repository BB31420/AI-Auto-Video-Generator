# AI-Auto-Video-Generator
An AI-powered storytelling video generator that takes user input as a story prompt, generates a story using OpenAI's GPT-3, creates images using OpenAI's DALL-E, adds voiceover using ElevenLabs API, and combines the elements into a video.


[![Example 0](https://img.youtube.com/vi/bNzlbGV2SvA/0.jpg)](https://www.youtube.com/watch?v=bNzlbGV2SvA)
[![Example 1](https://img.youtube.com/vi/b-zo4Laj-Ks/0.jpg)](https://www.youtube.com/watch?v=b-zo4Laj-Ks)
[![Example 2](https://img.youtube.com/vi/ExBBwcFDId0/0.jpg)](https://www.youtube.com/watch?v=ExBBwcFDId0)




## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

- Python 3.6 or higher
- Pip (Python package manager)
- FFmpeg (a command-line program for video processing)

### Installation

1. Clone the repository: ```git clone https://github.com/BB31420/AI-Auto-Video-Generator.git```
2. Navigate to the project directory: ```cd AI-Auto-Video-Generator```
3. Install the required Python packages: ```pip install -r requirements.txt```
4. Install FFmpeg:
 - On macOS, you can use Homebrew: brew install ffmpeg
 - On Linux, you can use your package manager (e.g., apt-get install ffmpeg on Ubuntu)
 - On Windows, you can download an installer from the official FFmpeg website


### Usage

1. Edit the file named .env in the project directory and add your API keys: 

`OPENAI_API_KEY=your_openai_api_key`

`ELEVENLABS_API_KEY=your_elevenlabs_api_key`

Replace your_openai_api_key and your_elevenlabs_api_key with your actual API keys.

2. Run the autovideo.py script by navigating to the directory the script and .env file are saved. Output will be generated in the same folder: 

`python main.py`

3. Follow the prompts to enter a story prompt and generate a video.

### Troubleshooting
* If you encounter errors related to missing dependencies, make sure you have installed the required Python packages by running `pip install -r requirements.txt`
* If you encounter errors related to FFmpeg, make sure it is installed on your system and available in your system's PATH.

 
 
 


# Instructable: Modifying the Code for Haikus and Bee Facts

This instructable will guide you through modifying the provided code to focus on generating haikus and fact-based videos about bees. We'll cover changing the prompt, the models, text overlay, and background color and positioning.

1. **Changing the prompt**
 * For haikus, replace the user input prompt with a fixed prompt related to haikus: 
```
story_prompt = "Create a haiku about nature"
```

* For bee facts, use a fixed prompt related to bees: 
```
story_prompt = "Tell me 5 interesting facts about bees"
```
2. **Changing the models**

To change the model, replace the engine parameter in the openai.Completion.create() function. For example, use the text-curie-002 model:
```
response = openai.Completion.create(
    engine="text-curie-002",
    prompt=prompt,
    max_tokens=400,
    n=1,
    stop=None,
    temperature=0.7,
)
```
3. **Changing text overlay and background color**

Modify the add_text_to_image() function to change text overlay and background color:
* For haikus, set the font size to a smaller value, and change text color to a dark green and background color to a lighter green:
``` 
font = ImageFont.truetype("Gabriola.ttf", size=30)```
text_color = (30, 120, 60)
bg_color = (200, 255, 200, 120)
```
* For bee facts, set the font size to a smaller value, and change text color to a dark yellow and background color to a lighter yellow:
```
font = ImageFont.truetype("Gabriola.ttf", size=30)
text_color = (180, 180, 0)
bg_color = (255, 255, 200, 120)
```
4. **Positioning text overlay**
* Modify the add_text_to_image() function to change the positioning of the text overlay. For example, to position the text in the center of the image, update the y_position calculation:
```
y_position = (image.height - text_height) // 2
```
5. **Changing the duration of each image**
* To change the duration of each image, modify the set_duration() parameter in the create_video() function. For example, set the duration to 5 seconds per image:
```
image_clips = [mpy.ImageClip(img).set_duration(5) for img in image_filenames]
```
6 . **Changing the number of images**
* To change the number of images, update the num_prompts parameter in the extract_image_prompts() function. For example, to generate 6 images, change the function call as follows:
 ```
image_prompts = extract_image_prompts(story, num_prompts=6)
```
7. **Changing the voice used for the voiceover**
* To change the voice for the voiceover, modify the generate_voiceover() function. Update the URL used in the requests.post() call with the desired voice ID. For example, to use a different voice, replace the existing voice ID with a new one (e.g., "21m00Tcm4TlvDq8ikWAM", "yoZ06aMxZJJ28mfd3POQ", or "AZnzlk1XvdvUeBnXmlld"):
```
response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/NEW_VOICE_ID", headers=headers, json=data)
```

Now, you can modify the code based on the provided instructions to generate haikus or fact-based videos about bees, with the desired duration for each image, the number of images, and the voice used for the voiceover. Remember to customize the prompts, models, text overlay, background color and positioning, image duration, image count, and voiceover based on your requirements.

Additionally, be mindful of the token limits for your API usage, as exceeding these limits may result in additional charges. You can adjust the max_tokens parameter in the openai.Completion.create() function to control the length of the generated text. Consider setting a lower value to stay within your API limits, especially when generating longer stories or facts.
