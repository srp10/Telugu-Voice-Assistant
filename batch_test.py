#!/usr/bin/env python3
"""
Batch Testing Script for Telugu Voice Banking Assistant
========================================================
Test multiple audio files and generate a report.

Usage:
    python batch_test.py --audio-dir ./test_audio/
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from voice_banking_assistant import TeluguVoiceBankingAssistant


class BatchTester:
    """Batch testing framework for voice banking assistant"""

    def __init__(self, assistant: TeluguVoiceBankingAssistant, output_dir: str = "test_results"):
        self.assistant = assistant
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []

    def test_audio_file(self, audio_path: str, metadata: Dict = None) -> Dict:
        """
        Test a single audio file and collect metrics

        Args:
            audio_path: Path to audio file
            metadata: Optional metadata (speaker info, expected text, etc.)

        Returns:
            Test result dictionary
        """
        print(f"\n{'='*70}")
        print(f"Testing: {audio_path}")
        print(f"{'='*70}")

        start_time = datetime.now()
        result = {
            'audio_file': audio_path,
            'timestamp': start_time.isoformat(),
            'metadata': metadata or {},
            'success': False
        }

        try:
            # Transcribe
            transcription = self.assistant.transcribe_audio(audio_path)
            result['transcription'] = transcription
            result['transcription_success'] = transcription is not None

            if transcription:
                # Process query
                response = self.assistant.process_banking_query(transcription)
                result['response'] = response
                result['response_success'] = response is not None

                if response:
                    # Generate TTS
                    output_file = self.output_dir / f"response_{Path(audio_path).stem}.mp3"
                    tts_file = self.assistant.text_to_speech(response, str(output_file))
                    result['tts_file'] = str(tts_file)
                    result['tts_success'] = tts_file is not None
                    result['success'] = True

        except Exception as e:
            result['error'] = str(e)
            print(f"❌ Error: {e}")

        # Calculate duration
        end_time = datetime.now()
        result['duration_seconds'] = (end_time - start_time).total_seconds()

        # Evaluate if ground truth provided
        if metadata and 'expected_transcription' in metadata:
            result['transcription_match'] = self._evaluate_transcription(
                transcription,
                metadata['expected_transcription']
            )

        self.results.append(result)
        return result

    def _evaluate_transcription(self, actual: str, expected: str) -> Dict:
        """Simple evaluation of transcription accuracy"""
        if not actual or not expected:
            return {'match': False, 'similarity': 0.0}

        # Simple word-level comparison
        actual_words = set(actual.lower().split())
        expected_words = set(expected.lower().split())

        if not expected_words:
            return {'match': False, 'similarity': 0.0}

        intersection = actual_words & expected_words
        similarity = len(intersection) / len(expected_words)

        return {
            'match': actual.lower() == expected.lower(),
            'similarity': similarity,
            'actual': actual,
            'expected': expected
        }

    def test_directory(self, audio_dir: str, metadata_file: str = None) -> List[Dict]:
        """
        Test all audio files in a directory

        Args:
            audio_dir: Directory containing audio files
            metadata_file: Optional JSON file with metadata for each file

        Returns:
            List of test results
        """
        audio_dir = Path(audio_dir)
        metadata_map = {}

        # Load metadata if provided
        if metadata_file and os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata_map = json.load(f)

        # Find all audio files
        audio_extensions = {'.mp3', '.wav', '.m4a', '.webm', '.ogg', '.flac'}
        audio_files = [
            f for f in audio_dir.iterdir()
            if f.suffix.lower() in audio_extensions
        ]

        print(f"\n🎯 Found {len(audio_files)} audio files to test\n")

        # Test each file
        for audio_file in sorted(audio_files):
            metadata = metadata_map.get(audio_file.name, {})
            self.test_audio_file(str(audio_file), metadata)

        return self.results

    def generate_report(self, output_file: str = None) -> Dict:
        """
        Generate a summary report of all tests

        Args:
            output_file: Optional file to save report

        Returns:
            Summary statistics
        """
        if not self.results:
            print("No test results to report")
            return {}

        total_tests = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        transcription_success = sum(1 for r in self.results if r.get('transcription_success'))
        response_success = sum(1 for r in self.results if r.get('response_success'))

        avg_duration = sum(r['duration_seconds'] for r in self.results) / total_tests

        summary = {
            'total_tests': total_tests,
            'successful': successful,
            'success_rate': successful / total_tests,
            'transcription_success_rate': transcription_success / total_tests,
            'response_success_rate': response_success / total_tests,
            'average_duration_seconds': avg_duration,
            'timestamp': datetime.now().isoformat(),
            'results': self.results
        }

        # Print summary
        print("\n" + "="*70)
        print("📊 TEST SUMMARY REPORT")
        print("="*70)
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful} ({summary['success_rate']*100:.1f}%)")
        print(f"Transcription Success: {transcription_success} ({summary['transcription_success_rate']*100:.1f}%)")
        print(f"Response Success: {response_success} ({summary['response_success_rate']*100:.1f}%)")
        print(f"Average Duration: {avg_duration:.2f} seconds")
        print("="*70)

        # Detailed results
        print("\n📋 DETAILED RESULTS:\n")
        for i, result in enumerate(self.results, 1):
            print(f"{i}. {Path(result['audio_file']).name}")
            print(f"   Status: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
            if result.get('transcription'):
                print(f"   Transcription: {result['transcription'][:50]}...")
            if result.get('error'):
                print(f"   Error: {result['error']}")
            print()

        # Save to file
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            print(f"💾 Detailed report saved to: {output_file}\n")

        return summary


def main():
    parser = argparse.ArgumentParser(
        description='Batch test Telugu Voice Banking Assistant'
    )
    parser.add_argument(
        '--audio-dir',
        type=str,
        required=True,
        help='Directory containing audio files to test'
    )
    parser.add_argument(
        '--metadata',
        type=str,
        help='JSON file with metadata (expected transcriptions, speaker info, etc.)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='test_results',
        help='Directory to save results (default: test_results)'
    )
    parser.add_argument(
        '--report',
        type=str,
        default='test_report.json',
        help='Report output file (default: test_report.json)'
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

    if not openai_key or not anthropic_key:
        print("❌ API keys not found!")
        print("\nSet environment variables:")
        print("  export OPENAI_API_KEY='your-key'")
        print("  export ANTHROPIC_API_KEY='your-key'")
        sys.exit(1)

    # Create assistant
    assistant = TeluguVoiceBankingAssistant(openai_key, anthropic_key)

    # Create tester
    tester = BatchTester(assistant, args.output_dir)

    # Run tests
    print(f"\n🚀 Starting batch tests on: {args.audio_dir}\n")
    tester.test_directory(args.audio_dir, args.metadata)

    # Generate report
    tester.generate_report(args.report)


if __name__ == '__main__':
    main()
