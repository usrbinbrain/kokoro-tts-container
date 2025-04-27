# Kokoro TTS Container

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/downloads/)
[![ONNX](https://img.shields.io/badge/ONNX-Runtime-lightgrey?logo=onnx)](https://onnxruntime.ai/)
[![Build and Push kokoro-tts-container](https://github.com/usrbinbrain/kokoro-tts-container/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/usrbinbrain/kokoro-tts-container/actions/workflows/build-and-push.yml)

A Docker container for running Kokoro Text-to-Speech engine v.1, providing high-quality speech synthesis with 54 voices and 9 languages options.

## Container Features

- [x] High-quality text-to-speech synthesis
- [x] Multiple voice and languages options
- [x] Voice blending capabilities
- [x] Adjustable speech speed
- [x] Support for .mp3 and .wav output files

## Quick Start Using Docker Hub Image

You can directly pull and run the pre-built container from Docker Hub without building locally:

```bash
# Pull the latest image
docker pull usrbinbrain/kokoro-tts-container:latest

# Run a basic example
docker run --rm -v $(pwd):/app/shared usrbinbrain/kokoro-tts-container \
    "Hello world!" \
    output.mp3 \
    --voice "af_sarah" \
    --speed 1.0 \
    --lang "en-us"
```

This way you can use Kokoro-TTS instantly without worrying about setup or build steps.

## Local Setup && Build 

Building your kokoro-tts Docker image:

```bash
# Install requirements for setup
pip3 install -r requirements.txt

# Run setup to donwload model and gerenate voices bin file
python3 setup.py

# Build your kokoro-tts image
docker build -t kokoro-tts-container .
```

## Usage

### Basic Usage Examples

Run the container with a single voice.

The command below generates an **output.mp3** file, where `af_sarah` voice says "**Hello my friend!**" in English (US) with speed `1.2`

```bash
docker run --rm -v $(pwd):/app/shared kokoro-tts-container \
    "Hello my friend!" \
    output.mp3 \
    --voice "af_sarah" \
    --speed 1.2 \
    --lang "en-us"
```

### Voice Blending

Kokoro-TTS supports voice blending, allowing you to mix multiple voices with different weights.

The command below generates an **output.wav** file with combined voices, where `af_sarah` contributes `40%` and `am_adam` contributes `60%` to the final voice saying "**Hasta la vista!**" in Spanish with speed `0.8`

```bash
docker run --rm -v $(pwd):/app/shared kokoro-tts-container \
    "Hasta la vista!" \
    output.wav \
    --voice "af_sarah:40,am_adam:60" \
    --speed 0.8 \
    --lang "es"
```

### Container Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input_text` | The text to synthesize | Required |
| `output_file` | Output audio filename (`.wav` or `.mp3`) | Required |
| `--voice` | [Voice ID](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) or blend (format: `voice1:weight,voice2:weight`) | `af_sarah` |
| `--speed` | Speech rate multiplier, allows `0.5` to `2.0` | `1.0` |
| `--lang` | Language code | `en-us` |

## Supported Languages and Codes

- `en-us`: English (US)
- `en-gb`: English (British)
- `fr-fr`: French
- `ja`: Japanese
- `hi`: Hindi
- `cmn`: Mandarin Chinese
- `es`: Spanish
- `pt-br`: Brazilian Portuguese
- `it`: Italian

## Available Voices

The container includes multiple voices for different languages, for a [complete list of voices](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) or another help, run:

```bash
docker run --rm kokoro-tts-container --help
```

## Thanks

Built with ❤️ on top of [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx) - A special thanks to [thewh1teagle](https://github.com/thewh1teagle) and [hexgrad](https://huggingface.co/hexgrad/Kokoro-82M) for providing this amazing fast TTS engine that made this container project possible.