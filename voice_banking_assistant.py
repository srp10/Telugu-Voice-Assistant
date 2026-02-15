#!/usr/bin/env python3
"""
Telugu Voice Banking Assistant
================================
A proof-of-concept voice banking system for Telugu speakers.

Architecture:
1. Speech-to-Text: OpenAI Whisper
2. Intent Understanding: Anthropic Claude
3. Text-to-Speech: Google TTS

Usage:
    python voice_banking_assistant.py --audio test.mp3
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Optional

try:
    import openai
    from anthropic import Anthropic
    from gtts import gTTS
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\nPlease install required packages:")
    print("  pip install openai anthropic gtts pydub python-dotenv --break-system-packages")
    sys.exit(1)

# Load configuration from .env file
load_dotenv(Path(__file__).parent / ".env")


class TeluguVoiceBankingAssistant:
    """Main class for Telugu Voice Banking Assistant"""

    def __init__(self, openai_key: str, anthropic_key: str):
        """
        Initialize the assistant with API keys

        Args:
            openai_key: OpenAI API key for Whisper
            anthropic_key: Anthropic API key for Claude
        """
        self.openai_client = openai.OpenAI(api_key=openai_key)
        self.anthropic_client = Anthropic(api_key=anthropic_key)

    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """
        Convert Telugu audio to text using OpenAI Whisper

        Args:
            audio_file_path: Path to audio file

        Returns:
            Transcribed text or None if error
        """
        try:
            print("🎙️  Transcribing audio...")

            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    prompt="Telugu language audio. తెలుగు భాష."
                )

            transcribed_text = transcript.text
            print("\n" + "="*70)
            print("📝 TRANSCRIPTION:")
            print("="*70)
            print(transcribed_text)
            print("="*70 + "\n")

            return transcribed_text

        except Exception as e:
            print(f"❌ Error during transcription: {e}")
            return None

    def process_banking_query(self, telugu_text: str) -> Optional[str]:
        """
        Understand Telugu banking question and generate response

        Args:
            telugu_text: Transcribed Telugu text

        Returns:
            Response in Telugu or None if error
        """
        if not telugu_text:
            print("❌ No text to process")
            return None

        try:
            print("🤔 Understanding the question and generating response...")

            prompt = f"""You are a helpful Telugu banking assistant for elderly customers.

The customer said (in Telugu): "{telugu_text}"

Please:
1. Identify what they're asking about (balance check, recent transactions, account number, help, etc.)
2. Provide a clear, respectful response in Telugu
3. For this demo, you can make up sample data (e.g., sample balance: ₹25,000)
4. Keep the response conversational and easy to understand
5. Use respectful terms appropriate for elderly users

Respond ONLY in Telugu, as if you're a real banking assistant."""

            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            print("\n" + "="*70)
            print("🤖 BANKING ASSISTANT RESPONSE:")
            print("="*70)
            print(response_text)
            print("="*70 + "\n")

            return response_text

        except Exception as e:
            print(f"❌ Error processing query: {e}")
            return None

    def text_to_speech(self, telugu_text: str, output_filename: str = "response.mp3") -> Optional[str]:
        """
        Convert Telugu text to speech

        Args:
            telugu_text: Text to convert
            output_filename: Output audio file path

        Returns:
            Path to audio file or None if error
        """
        if not telugu_text:
            print("❌ No text to convert to speech")
            return None

        try:
            print("🔊 Converting response to speech...")

            # Strip markdown formatting so TTS doesn't read "asterisk" aloud
            clean_text = re.sub(r'\*+', '', telugu_text)       # remove * and **
            clean_text = re.sub(r'#+\s?', '', clean_text)      # remove # headings
            clean_text = re.sub(r'`+', '', clean_text)         # remove backticks
            clean_text = re.sub(r'\n{3,}', '\n\n', clean_text) # collapse extra newlines

            # Create TTS object
            tts = gTTS(text=clean_text, lang='te', slow=False)

            # Save to file
            tts.save(output_filename)

            print(f"✅ Audio saved as: {output_filename}")

            return output_filename

        except Exception as e:
            print(f"❌ Error creating speech: {e}")
            return None

    def process_voice_query(self, audio_file_path: str, output_audio: str = "response.mp3") -> bool:
        """
        Complete pipeline: Voice input → Voice output

        Args:
            audio_file_path: Input audio file path
            output_audio: Output audio file path

        Returns:
            True if successful, False otherwise
        """
        print("\n" + "="*70)
        print("🚀 STARTING COMPLETE VOICE BANKING TEST")
        print("="*70 + "\n")

        # Step 1: Transcribe
        print("Step 1/3: Speech to Text")
        transcribed = self.transcribe_audio(audio_file_path)
        if not transcribed:
            return False

        # Step 2: Process query
        print("\nStep 2/3: Understanding Question & Generating Response")
        response = self.process_banking_query(transcribed)
        if not response:
            return False

        # Step 3: Text to speech
        print("\nStep 3/3: Converting Response to Speech")
        audio_out = self.text_to_speech(response, output_audio)

        if audio_out:
            print("\n" + "="*70)
            print("✅ COMPLETE! Test finished successfully.")
            print(f"🎧 Play the response: {output_audio}")
            print("="*70)
            return True
        else:
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Telugu Voice Banking Assistant - Test a voice query'
    )
    parser.add_argument(
        '--audio',
        type=str,
        help='Path to Telugu audio file (mp3, wav, m4a, etc.)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='response.mp3',
        help='Output audio file path (default: response.mp3)'
    )
    parser.add_argument(
        '--openai-key',
        type=str,
        help='OpenAI API key (or set OPENAI_API_KEY env var)'
    )
    parser.add_argument(
        '--anthropic-key',
        type=str,
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )

    args = parser.parse_args()

    # Get API keys
    openai_key = args.openai_key or os.getenv('OPENAI_API_KEY')
    anthropic_key = args.anthropic_key or os.getenv('ANTHROPIC_API_KEY')

    if not openai_key:
        print("❌ OpenAI API key not found!")
        print("\nSet it using:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("  or use --openai-key flag")
        sys.exit(1)

    if not anthropic_key:
        print("❌ Anthropic API key not found!")
        print("\nSet it using:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        print("  or use --anthropic-key flag")
        sys.exit(1)

    # Check audio file
    if not args.audio:
        print("❌ No audio file specified!")
        print("\nUsage:")
        print("  python voice_banking_assistant.py --audio test.mp3")
        sys.exit(1)

    if not os.path.exists(args.audio):
        print(f"❌ Audio file not found: {args.audio}")
        sys.exit(1)

    # Create assistant and process
    assistant = TeluguVoiceBankingAssistant(openai_key, anthropic_key)
    success = assistant.process_voice_query(args.audio, args.output)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
