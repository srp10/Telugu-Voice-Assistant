# Telugu Voice Banking Assistant

A proof-of-concept voice banking system for elderly Telugu speakers. It enables users to speak banking queries in Telugu and receive natural voice responses — all powered by modern AI.

## Architecture

```
Telugu Audio Input
       |
       v
 OpenAI Whisper ──────── Speech-to-Text
       |
       v
 Anthropic Claude ────── Intent Understanding + Response Generation
       |
       v
 Google TTS (gTTS) ───── Text-to-Speech
       |
       v
Telugu Audio Response
```

**Pipeline**: User speaks in Telugu → Whisper transcribes → Claude understands the banking query and generates a Telugu response → gTTS converts the response back to audio.

## Features

- Speech-to-text for Telugu using OpenAI Whisper
- Banking intent understanding and response generation using Anthropic Claude
- Text-to-speech output in Telugu using Google TTS
- End-to-end voice pipeline (audio in → audio out)
- Batch testing framework for multiple audio files
- Support for code-switched queries (Telugu + English)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/srp10/Telugu-Voice-Assistant.git
cd Telugu-Voice-Assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up API keys

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Then edit `.env` with your keys:

```env
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

Or export them as environment variables:

```bash
export OPENAI_API_KEY='your-openai-api-key'
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

### 4. Run

```bash
python voice_banking_assistant.py --audio your_audio.mp3
```

## Usage

### Basic usage

```bash
python voice_banking_assistant.py --audio balance_check.mp3
```

### Custom output file

```bash
python voice_banking_assistant.py --audio balance_check.mp3 --output my_response.mp3
```

### Pass API keys as arguments

```bash
python voice_banking_assistant.py \
  --audio test.mp3 \
  --openai-key 'sk-proj-...' \
  --anthropic-key 'sk-ant-...'
```

### Batch testing

```bash
python batch_test.py --audio-dir ./test_audio/ --report results.json
```

### Use as a Python library

```python
from voice_banking_assistant import TeluguVoiceBankingAssistant

assistant = TeluguVoiceBankingAssistant(
    openai_key='your-openai-key',
    anthropic_key='your-anthropic-key'
)

# Full pipeline
assistant.process_voice_query('audio.mp3', 'response.mp3')

# Or use individual components
transcribed = assistant.transcribe_audio('audio.mp3')
response = assistant.process_banking_query(transcribed)
audio_file = assistant.text_to_speech(response, 'output.mp3')
```

## Sample Telugu Banking Queries

| Query | Telugu | Translation |
|-------|--------|-------------|
| Balance check | నా ఖాతా బ్యాలెన్స్ ఎంత? | What's my account balance? |
| Recent transactions | నా చివరి లావాదేవీలు చూపించండి | Show my recent transactions |
| Account number | నా ఖాతా సంఖ్య ఏమిటి? | What's my account number? |
| Help | నాకు సహాయం కావాలి | I need help |
| Mini statement | నా మినీ స్టేట్‌మెంట్ పంపించండి | Send my mini statement |

## Project Structure

```
├── voice_banking_assistant.py     # Main assistant script
├── batch_test.py                  # Batch testing framework
├── requirements.txt               # Python dependencies
├── example_metadata.json          # Example test data structure
├── README_LOCAL.md                # Local setup guide
├── PROJECT_OVERVIEW.md            # Detailed project overview
├── DEVELOPMENT_IDEAS.md           # Research directions & ideas
└── files/
    ├── telugu_voice_banking_assistant.ipynb  # Original Colab notebook
    └── SETUP_GUIDE.md                        # Colab setup guide
```

## Cost Estimate

| Service | Cost | Free Tier |
|---------|------|-----------|
| OpenAI Whisper | ~$0.006/min of audio | $5 credit |
| Anthropic Claude | ~$0.01/request | $5 credit |
| Google TTS (gTTS) | Free | Unlimited |
| **Total (20 queries)** | **~$2-3** | **$10 combined** |

## Requirements

- Python 3.8+
- OpenAI API key (for Whisper speech-to-text)
- Anthropic API key (for Claude intent understanding)

## License

Research / Educational Use
