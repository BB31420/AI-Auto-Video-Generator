# AI-Auto-Video-Generator
An AI-powered storytelling video generator that takes user input as a story prompt, generates a story using OpenAI's GPT-3, creates images using OpenAI's DALL-E, adds voiceover using ElevenLabs API, and combines the elements into a video.

The project is organized into modular components for better maintainability and follows best practices for handling API keys.

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

- Python 3.6 or higher
- Pip (Python package manager)

### Installation

1. Clone the repository: ```git clone https://github.com/yourusername/AI-Storyteller-Video-Generator.git```
2. Navigate to the project directory: ```cd AI-Storyteller-Video-Generator```
3. Install the required Python packages: ```pip install -r requirements.txt```
4. Create a new file named `.env` in the project directory and add your API keys:
```OPENAI_API_KEY=your_openai_api_key```
```ELEVENLABS_API_KEY=your_elevenlabs_api_key```

Replace `your_openai_api_key` and `your_elevenlabs_api_key` with your actual API keys.

### Usage

Run the `autovideo.py` script by navigating to the directory the script and `.env` are saved. Output will be generated in the same folder:

```python autovideo.py```





