# OpenAI-Compatible Edge-TTS API (SkyrimNet Bangla Fork) 🗣️

![GitHub stars](https://img.shields.io/github/stars/travisvn/openai-edge-tts?style=social)
![GitHub forks](https://img.shields.io/github/forks/travisvn/openai-edge-tts?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/travisvn/openai-edge-tts)
![GitHub top language](https://img.shields.io/github/languages/top/travisvn/openai-edge-tts)
![GitHub last commit](https://img.shields.io/github/last-commit/travisvn/openai-edge-tts?color=red)
[![Discord](https://img.shields.io/badge/Discord-Voice_AI_%26_TTS_Tools-blue?logo=discord&logoColor=white)](https://discord.gg/GkFbBCBqJ6)
[![LinkedIn](https://img.shields.io/badge/Connect_on_LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/travisvannimwegen)

This fork extends [`travisvn/openai-edge-tts`](https://github.com/travisvn/openai-edge-tts) with a custom **SkyrimNet Bangla Bridge (`skyrim_bridge.py`)** and **1-Click Windows Launcher (`Start_Bangla_TTS.bat`)**, allowing **SkyrimNet** to use free Microsoft Edge **Bangla (`bn-BD`)** neural voices without paid APIs or GPU VRAM.

---

## 🎮 SkyrimNet Bangla Bridge Setup (Added in This Fork)

### What Was Changed & Added
1. **`skyrim_bridge.py` (Port `5055`):**
   - **Fixes `"TTS failed to generate audio"` in SkyrimNet:** SkyrimNet's `OpenAI-Compatible` engine requires a Boson.ai / Higgs-style `/v1/audio/voices` enrollment JSON response before generating speech. `skyrim_bridge.py` handles `POST /v1/audio/voices` and forwards `POST /v1/audio/speech` directly to `edge-tts`.
   - **Automatic Gender-to-Bangla Voice Mapping:** Automatically maps incoming Skyrim internal voice IDs (`malecommoner`, `femaleeventoned`, `femaleargonian`, etc.) to Microsoft Edge Bangla voices:
     - **Female NPCs:** `bn-BD-NabanitaNeural`
     - **Male NPCs:** `bn-BD-PradeepNeural`
   - **No API Key Required:** Works out of the box without bearer token authentication errors.
2. **`Start_Bangla_TTS.bat`:**
   - 1-click Windows launcher that navigates to the folder (`cd /d "%~dp0"`), activates `venv\Scripts\activate`, and starts `skyrim_bridge.py`.

### Quick Start for SkyrimNet (Windows)

#### 1. First-Time Setup
Open Command Prompt inside this folder and install the dependencies:
```cmd
python -m venv venv
venv\Scripts\activate
pip install flask edge-tts
```

#### 2. Run the SkyrimNet Bridge
Double-click **`Start_Bangla_TTS.bat`** (or run manually in terminal):
```cmd
cd path\(\to\openai-\)edge-tts-main
venv\Scripts\activate
python skyrim_bridge.py
```
Keep the terminal window open while playing Skyrim (`http://127.0.0.1:5055`).

#### 3. Configure SkyrimNet (`http://localhost:8080`)
1. Open the SkyrimNet web dashboard (`http://localhost:8080`) and go to **Text-to-Speech**.
2. Set **TTS Engine** to **`OpenAI-Compatible`**.
3. Set **Endpoint** to **`http://localhost:5055`**.
4. Set **Model** to **`tts-1`**.
5. *(Optional)* In **LLM / Prompts**, add: `Always respond in natural spoken Bengali (বাংলা script).`
6. Click **Save** and **Test TTS**.

---

## Original Project Documentation

This project provides a local, OpenAI-compatible text-to-speech (TTS) API using `edge-tts`. It emulates the OpenAI TTS endpoint (`/v1/audio/speech`), enabling users to generate speech from text with various voice options and playback speeds, just like the OpenAI API.

`edge-tts` uses Microsoft Edge's online text-to-speech service, so it is completely free.

[View this project on Docker Hub](https://hub.docker.com/r/travisvn/openai-edge-tts)

### Features

- **OpenAI-Compatible Endpoint**: `/v1/audio/speech` with similar request structure and behavior.
- **SSE Streaming Support**: Real-time audio streaming via Server-Sent Events when `stream_format: "sse"` is specified.
- **Supported Voices**: Maps OpenAI voices (alloy, echo, fable, onyx, nova, shimmer) to `edge-tts` equivalents.
- **Flexible Formats**: Supports multiple audio formats (mp3, opus, aac, flac, wav, pcm).
- **Adjustable Speed**: Option to modify playback speed (0.25x to 4.0x).
- **Optional Direct Edge-TTS Voice Selection**: Use either OpenAI voice mappings or specify [any edge-tts voice](https://tts.travisvn.com) directly.

### ⚡️ Quick start (Docker)

The simplest way to get started without having to configure anything is to run the command below:

```bash
docker run -d -p 5050:5050 travisvn/openai-edge-tts:latest
```

This will run the service at port 5050 with all the default configs _(Docker required)_.

### Setup

#### Prerequisites

- **Docker** (recommended): Docker and Docker Compose for containerized setup.
- **Python** (optional): For local development, install dependencies in `requirements.txt`.
- **ffmpeg** (optional): Required for audio format conversion. Optional if sticking to mp3.

#### Installation

1. **Clone the Repository**:

```bash
git clone https://github.com/travisvn/openai-edge-tts.git
cd openai-edge-tts
```

2. **Environment Variables**: Create a `.env` file in the root directory with the following variables:

```env
API_KEY=your_api_key_here
PORT=5050

DEFAULT_VOICE=en-US-AvaNeural
DEFAULT_RESPONSE_FORMAT=mp3
DEFAULT_SPEED=1.0

DEFAULT_LANGUAGE=en-US

REQUIRE_API_KEY=True
REMOVE_FILTER=False
EXPAND_API=True
DETAILED_ERROR_LOGGING=True
```

Or copy the default `.env.example`:

```bash
cp .env.example .env
```

3. **Run with Docker Compose** (recommended):

```bash
docker compose up -d
```

<details>
<summary>

#### Building Locally with FFmpeg using Docker Compose

</summary>

By default, `docker compose up --build` creates a minimal image _without_ `ffmpeg`. If you're building locally (after cloning this repository) and need `ffmpeg` for audio format conversions (beyond MP3), you can include it in the build using `INSTALL_FFMPEG_ARG=true`:

```bash
INSTALL_FFMPEG_ARG=true docker compose up --build
```

For pre-built Docker Hub images, add the `latest-ffmpeg` tag:

```bash
docker run -d -p 5050:5050 -e API_KEY=your_api_key_here -e PORT=5050 travisvn/openai-edge-tts:latest-ffmpeg
```

</details>

4. **Access the API**: Your server will be accessible at `http://localhost:5050`.

<details>
<summary>

### Running Original Server with Python

</summary>

1. **Set Up a Virtual Environment**:
```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the Server**:
```bash
python app/server.py
```
The server will start running at `http://localhost:5050`.

</details>

<details>
<summary>

### Usage

</summary>

#### Endpoint: `/v1/audio/speech`

Generates audio from the input text.

- **input** (string, required): The text to be converted to audio (up to 4096 characters).
- **model** (string, optional): Set to `"tts-1"` or `"tts-1-hd"` (default: `"tts-1"`).
- **voice** (string, optional): OpenAI-compatible voice (`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`) or any valid `edge-tts` voice.
- **response_format** (string, optional): `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm` (default: `mp3`).
- **speed** (number, optional): Playback speed (`0.25` to `4.0`, default: `1.0`).
- **stream_format** (string, optional): `"audio"` (default) or `"sse"`.

#### Standard Audio Generation Example

```bash
curl -X POST http://localhost:5050/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key_here" \
  -d '{
    "input": "Hello, I am your AI assistant!",
    "voice": "echo",
    "response_format": "mp3",
    "speed": 1.1
  }' \
  --output speech.mp3
```

#### Additional Endpoints

- **POST/GET `/v1/models`**: Lists available TTS models.
- **POST/GET `/v1/voices`**: Lists edge-tts voices for a given language / locale.
- **POST/GET `/v1/voices/all`**: Lists all edge-tts voices with language support information.

</details>

### License

This project is licensed under GNU General Public License v3.0 (GPL-3.0).
