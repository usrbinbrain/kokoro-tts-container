#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import itertools
import threading
import argparse
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
supported_languages = {
    "en-us": "English",
    "en-gb": "English (British)",
    "fr-fr": "French",
    "ja": "Japanese",
    "hi": "Hindi",
    "cmn": "Mandarin Chinese",
    "es": "Spanish",
    "pt-br": "Brazilian Portuguese",
    "it": "Italian",
}
MODEL_FILENAME = "kokoro_v1.onnx"
VOICES_FILENAME = "voices_v1.bin"
OUTPUT_DIR = "/app/shared"
stop_spinner = False

def start_spinner():
    global stop_spinner
    stop_spinner = False
    spinner_thread = threading.Thread(target=spinning_wheel, args=("Synthesizing text to audio...",))
    spinner_thread.start()
    return spinner_thread

def stop_spinner_thread():
    global stop_spinner
    stop_spinner = True

def spinning_wheel(message="Synthesizing text to audio...", progress=None):
    spinner = itertools.cycle(['⠋ ', '⠙ ', '⠹ ', '⠸ ', '⠼ ', '⠴ ', '⠦ ', '⠧ ', '⠇ ', '⠏ '])
    while not stop_spinner:
        spin = next(spinner)
        if progress is not None:
            sys.stdout.write(f"\r{message} {progress} {spin}")
        else:
            sys.stdout.write(f"\r{message} {spin}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(message) + 50) + '\r')
    sys.stdout.flush()

def validate_voice(voice, kokoro):
    supported_voices = set(kokoro.get_voices())
    if ',' in voice:
        voices = []
        weights = []
        for pair in voice.split(','):
            if ':' in pair:
                v, w = pair.strip().split(':')
                voices.append(v.strip())
                weights.append(float(w.strip()))
            else:
                voices.append(pair.strip())
                weights.append(50.0)  # Default 50% weight
        if len(voices) != 2:
            raise ValueError("Voice blending requires exactly two voices separated by comma (eg. 'af_sarah:60,am_adam:40').")
        for v in voices:
            if v not in supported_voices:
                supported_list = ', '.join(sorted(supported_voices))
                raise ValueError(f"Voice not supported: {v}\nSupported voices: {supported_list}")
        total = sum(weights)
        if total != 100:
            weights = [w * (100 / total) for w in weights]
        style1 = kokoro.get_voice_style(voices[0])
        style2 = kokoro.get_voice_style(voices[1])
        blend = np.add(style1 * (weights[0] / 100), style2 * (weights[1] / 100))
        return blend
    else:
        if voice not in supported_voices:
            supported_list = ', '.join(sorted(supported_voices))
            raise ValueError(f"Voice not supported: {voice}\nSupported voices: {supported_list}")
        return voice

def generate_audio(text, voice="af_sarah", speed=1.0, lang="en-us"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, MODEL_FILENAME)
    voices_path = os.path.join(current_dir, VOICES_FILENAME)
    kokoro = Kokoro(model_path, voices_path)
    validated_voice = validate_voice(voice, kokoro)
    audio, sample_rate = kokoro.create(text, voice=validated_voice, speed=speed, lang=lang)
    return audio, sample_rate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Kokoro-tts-container, text to speech container with 54 voices and 9 languages",
        usage="docker run --rm -v $(pwd):/app/shared IMAGE_NAME \"input_text\" output_file [options]"
    )
    parser.add_argument("input_text", type=str, help="Text to be synthesized to audio")
    parser.add_argument("output_file", type=str, help="Audio output file, with .mp3 or .wav extension")
    parser.add_argument("--voice", type=str, default="af_sarah", help="Voice name to be used (supports blends, e.g.: 'af_sarah:60,am_adam:40')")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed, 0.5 to 2.0 (default: 1.0)")
    parser.add_argument("--lang", type=str, default="en-us", help=f"Synthesis language (default: en-us), avaliable: {', '.join(f"{v} ({k})" for k, v in supported_languages.items())}")
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        voices = sorted(Kokoro(MODEL_FILENAME, VOICES_FILENAME).get_voices())
        parser.epilog = f"Available voices: {', '.join(voices)}"
    args = parser.parse_args()
    spinner_thread = start_spinner()
    try:
        audio, sr = generate_audio(args.input_text, args.voice, args.speed, args.lang)
    except Exception as e:
        stop_spinner_thread()
        spinner_thread.join()
        print(f"\nError in synthesis: {e}")
        sys.exit(1)
    sf.write(f"{OUTPUT_DIR}/{args.output_file}", audio, sr)
    stop_spinner_thread()
    spinner_thread.join()
    print(f"[+] Audio file save in: {args.output_file}")
