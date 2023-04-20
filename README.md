# AI-Auto-Video-Generator
An AI-powered storytelling video generator that takes user input as a story prompt, generates a story using OpenAI's GPT-3, creates images using OpenAI's DALL-E, adds voiceover using ElevenLabs API, and combines the elements into a video.

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

- Python 3.6 or higher
- Pip (Python package manager)
- FFmpeg (a command-line program for video processing)

### Installation

1. Clone the repository: ```git clone https://github.com/yourusername/AI-Storyteller-Video-Generator.git```
2. Navigate to the project directory: ```cd AI-Auto-Video-Generator```
3. Install the required Python packages: ```pip install -r requirements.txt```
4. Install FFmpeg:
 - On macOS, you can use Homebrew: brew install ffmpeg
 - On Linux, you can use your package manager (e.g., apt-get install ffmpeg on Ubuntu)
 - On Windows, you can download an installer from the official FFmpeg website


### Usage

1. Create a new file named .env in the project directory and add your API keys: 

`OPENAI_API_KEY=your_openai_api_key`

`ELEVENLABS_API_KEY=your_elevenlabs_api_key`

Replace your_openai_api_key and your_elevenlabs_api_key with your actual API keys.

2. Run the autovideo.py script by navigating to the directory the script and .env file are saved. Output will be generated in the same folder: 

`python autovideo.py`

3. Follow the prompts to enter a story prompt and generate a video.

### Troubleshooting
* If you encounter errors related to missing dependencies, make sure you have installed the required Python packages by running `pip install -r requirements.txt`
* If you encounter errors related to FFmpeg, make sure it is installed on your system and available in your system's PATH.


