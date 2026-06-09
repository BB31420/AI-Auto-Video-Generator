"""Voiceover generation with pluggable TTS backends (60db + ElevenLabs).

Both providers expose the exact same contract -- they take the story text and
return the raw MP3 bytes (or ``None`` on failure) -- so everything downstream
(``create_video``/``save_voiceover``) stays identical no matter which backend
runs.

Provider selection
------------------
The ``TTS_PROVIDER`` env var picks the *primary* provider ("60db" or
"elevenlabs"). If the primary fails or has no API key, the code automatically
falls back to the other provider, so a single misconfigured key never breaks a
run. Default primary is "60db".
"""

import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()

# Shared, provider-neutral settings so both backends say/sound the same thing.
OUTRO = "..Comment with your favorite fact..."
# Normalized 0.0-1.0 voice knobs, mapped to each provider's own scale below.
STABILITY = 0.3
SIMILARITY = 0.3

SIXTYDB_TTS_URL = "https://api.60db.ai/tts-synthesize"
SIXTYDB_VOICES_URL = "https://api.60db.ai/myvoices"
ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"
# Default ElevenLabs voice (unchanged from the original implementation).
ELEVENLABS_VOICE_ID = "AZnzlk1XvdvUeBnXmlld"


def _sixtydb_tts(text):
    """Synthesize via 60db. Returns MP3 bytes, or None on error."""
    api_key = os.getenv("SIXTYDB_API_KEY")
    if not api_key:
        print("60db: SIXTYDB_API_KEY not set, skipping.")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "output_format": "mp3",
        "stability": int(STABILITY * 100),   # 60db uses a 0-100 scale
        "similarity": int(SIMILARITY * 100),
    }
    # Use the system default voice unless a specific voice_id is configured.
    voice_id = os.getenv("SIXTYDB_VOICE_ID")
    if voice_id:
        data["voice_id"] = voice_id

    try:
        response = requests.post(SIXTYDB_TTS_URL, headers=headers, json=data, timeout=120)
    except requests.RequestException as exc:
        print(f"60db: request failed ({exc}).")
        return None

    if response.status_code != 200:
        print(f"60db: error status code {response.status_code}: {response.text[:200]}")
        return None

    try:
        payload = response.json()
    except ValueError:
        print("60db: response was not valid JSON.")
        return None

    if not payload.get("success", True) or not payload.get("audio_base64"):
        print(f"60db: no audio returned ({payload.get('message', 'unknown error')}).")
        return None

    return base64.b64decode(payload["audio_base64"])


def _elevenlabs_tts(text):
    """Synthesize via ElevenLabs. Returns MP3 bytes, or None on error."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("ElevenLabs: ELEVENLABS_API_KEY not set, skipping.")
        return None

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
    }
    data = {
        "text": text,
        "voice_settings": {"stability": STABILITY, "similarity_boost": SIMILARITY},
    }
    url = f"{ELEVENLABS_TTS_URL}/{ELEVENLABS_VOICE_ID}"

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
    except requests.RequestException as exc:
        print(f"ElevenLabs: request failed ({exc}).")
        return None

    if response.status_code != 200:
        print(f"ElevenLabs: error status code {response.status_code}: {response.text[:200]}")
        return None

    return response.content


# Registry of available backends, keyed by the accepted TTS_PROVIDER values.
_PROVIDERS = {
    "60db": _sixtydb_tts,
    "sixtydb": _sixtydb_tts,
    "elevenlabs": _elevenlabs_tts,
    "11labs": _elevenlabs_tts,
}


def _provider_order():
    """Return [primary, fallback] backend callables based on TTS_PROVIDER."""
    primary = os.getenv("TTS_PROVIDER", "60db").strip().lower()
    primary_fn = _PROVIDERS.get(primary, _sixtydb_tts)
    # The fallback is whichever distinct backend isn't the primary.
    fallback_fn = _elevenlabs_tts if primary_fn is _sixtydb_tts else _sixtydb_tts
    return [primary_fn, fallback_fn]


def generate_voiceover(story, save_file=False):
    """Generate an MP3 voiceover for ``story``.

    Tries the configured primary provider first and transparently falls back to
    the other if it fails. Returns the raw MP3 bytes, or ``None`` if every
    provider failed.
    """
    text = story + OUTRO

    for backend in _provider_order():
        audio = backend(text)
        if audio:
            if save_file:
                with open("file.mp3", "wb") as f:
                    f.write(audio)
            return audio

    print("All TTS providers failed.")
    return None


def save_voiceover(voiceover_content, timestamp):
    voiceover_filename = f"voiceover_{timestamp}.mp3"
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)


def get_my_voices():
    """List the 60db voices available to your account.

    Helper for discovering a real ``voice_id`` to put in SIXTYDB_VOICE_ID.
    Returns a list of voice dicts (with ``voice_id``, ``name``, ``labels`` ...),
    or an empty list on error.
    """
    api_key = os.getenv("SIXTYDB_API_KEY")
    if not api_key:
        print("60db: SIXTYDB_API_KEY not set.")
        return []

    try:
        response = requests.get(
            SIXTYDB_VOICES_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30,
        )
    except requests.RequestException as exc:
        print(f"60db: voices request failed ({exc}).")
        return []

    if response.status_code != 200:
        print(f"60db: voices error status code {response.status_code}: {response.text[:200]}")
        return []

    voices = response.json().get("data", [])
    for v in voices:
        labels = v.get("labels", {})
        print(f"{v.get('voice_id')}  |  {v.get('name')}  |  "
              f"{labels.get('language_name')} {labels.get('gender')}  |  {v.get('model')}")
    return voices


if __name__ == "__main__":
    # Quick manual check: `python voiceover_generator.py` lists your 60db voices.
    get_my_voices()
