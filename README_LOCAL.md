# Telugu Voice Banking Assistant - Local Setup

## 🚀 Quick Start (Local Machine)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or if you need the `--break-system-packages` flag:
```bash
pip install openai anthropic gtts pydub --break-system-packages
```

### 2. Set Up API Keys

#### Option A: Environment Variables (Recommended)
```bash
export OPENAI_API_KEY='sk-proj-your-key-here'
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

#### Option B: Command Line Arguments
```bash
python voice_banking_assistant.py \
  --audio test.mp3 \
  --openai-key 'your-openai-key' \
  --anthropic-key 'your-anthropic-key'
```

### 3. Run a Test

```bash
python voice_banking_assistant.py --audio your_audio_file.mp3
```

This will:
1. Transcribe your Telugu audio to text
2. Generate a banking response in Telugu
3. Convert the response to speech (saved as `response.mp3`)

---

## 📝 Usage Examples

### Basic Usage
```bash
python voice_banking_assistant.py --audio balance_check.mp3
```

### Custom Output File
```bash
python voice_banking_assistant.py \
  --audio balance_check.mp3 \
  --output my_response.mp3
```

### With API Keys as Arguments
```bash
python voice_banking_assistant.py \
  --audio test.mp3 \
  --openai-key 'sk-proj-...' \
  --anthropic-key 'sk-ant-...'
```

---

## 🧪 Testing Sample Queries

Create audio files with these Telugu banking queries:

1. **Balance Check**: "నా ఖాతా బ్యాలెన్స్ ఎంత?" (What's my balance?)
2. **Transactions**: "నా చివరి లావాదేవీలు చూపించండి" (Show recent transactions)
3. **Account Number**: "నా ఖాతా సంఖ్య ఏమిటి?" (What's my account number?)
4. **Help**: "నాకు సహాయం కావాలి" (I need help)
5. **Mini Statement**: "నా మినీ స్టేట్‌మెంట్ పంపించండి" (Send mini statement)

---

## 🏗️ Project Structure

```
Telugu Voice Banking Assistant/
├── voice_banking_assistant.py  # Main script (converted from notebook)
├── telugu_voice_banking_assistant.ipynb  # Original Colab notebook
├── requirements.txt  # Python dependencies
├── SETUP_GUIDE.md  # Original Colab setup guide
├── README_LOCAL.md  # This file (local setup)
└── files/  # Original files
```

---

## 💡 Using as a Python Library

You can also import and use the assistant in your own code:

```python
from voice_banking_assistant import TeluguVoiceBankingAssistant

# Initialize
assistant = TeluguVoiceBankingAssistant(
    openai_key='your-openai-key',
    anthropic_key='your-anthropic-key'
)

# Process a voice query
assistant.process_voice_query('audio.mp3', 'response.mp3')

# Or use individual components
transcribed = assistant.transcribe_audio('audio.mp3')
response = assistant.process_banking_query(transcribed)
audio_file = assistant.text_to_speech(response, 'output.mp3')
```

---

## 🔍 Understanding the Code

### Main Components

1. **`transcribe_audio()`**
   - Uses OpenAI Whisper for speech-to-text
   - Supports Telugu language (language code: 'te')
   - Returns transcribed text

2. **`process_banking_query()`**
   - Uses Anthropic Claude to understand intent
   - Generates natural Telugu responses
   - Handles banking-specific queries

3. **`text_to_speech()`**
   - Uses Google TTS (gTTS) for free
   - Converts Telugu text to audio
   - Saves as MP3 file

4. **`process_voice_query()`**
   - Complete end-to-end pipeline
   - Orchestrates all three components

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install openai anthropic gtts pydub --break-system-packages
```

### "API key not found"
Make sure to set environment variables or use `--openai-key` and `--anthropic-key` flags

### "File not found"
Check that your audio file path is correct:
```bash
ls -la your_audio_file.mp3
```

### Audio file format issues
Supported formats: mp3, wav, m4a, webm, mpeg, mpga

Convert if needed:
```bash
ffmpeg -i input.m4a output.mp3
```

---

## 💰 Cost Tracking

- **Whisper API**: ~$0.006 per minute of audio
- **Claude API**: ~$0.01 per request
- **Google TTS**: Free

**Estimated cost for testing**: $2-3 for 10-20 queries

---

## 🔬 Next Steps for Development

See `DEVELOPMENT_IDEAS.md` for research directions and enhancement ideas.
