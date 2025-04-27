#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import io
import requests
import torch
import numpy as np
from tqdm import tqdm

# URLs e nomes de arquivos
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
MODEL_FILENAME = "kokoro_v1.onnx"
VOICES_FILENAME = "voices_v1.bin"

# Lista de todas as vozes disponíveis
supported_voices = [
    "af_heart", "af_alloy", "af_aoede", "af_bella", "af_jessica", "af_kore",
    "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael",
    "am_onyx", "am_puck", "am_santa",
    "bf_alice", "bf_emma", "bf_isabella", "bf_lily",
    "bm_daniel", "bm_fable", "bm_george", "bm_lewis",
    "jf_alpha", "jf_gongitsune", "jf_nezumi", "jf_tebukuro",
    "jm_kumo",
    "zf_xiaobei", "zf_xiaoni", "zf_xiaoxiao", "zf_xiaoyi",
    "zm_yunjian", "zm_yunxi", "zm_yunxia", "zm_yunyang",
    "ef_dora", "em_alex", "em_santa", "ff_siwis",
    "hf_alpha", "hf_beta", "hm_omega", "hm_psi",
    "if_sara", "im_nicola", "pf_dora", "pm_alex", "pm_santa",
]

def download_file(url, file_path):
    if os.path.exists(file_path):
        print(f"{file_path} já existe. Pulando download.")
        return
    with requests.get(url, stream=True, allow_redirects=True) as response:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 4096  # 4KB
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(file_path)) as progress:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(block_size):
                    progress.update(len(chunk))
                    f.write(chunk)

def download_model(path):
    model_file = os.path.join(path, MODEL_FILENAME)
    download_file(MODEL_URL, model_file)

def download_all_voices(path):
    voices_file = os.path.join(path, VOICES_FILENAME)
    if os.path.exists(voices_file):
        print(f"{voices_file} já existe. Pulando download de vozes.")
        return
    voices = {}
    url_pattern = "https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/voices/{name}.pt"
    for voice in supported_voices:
        url = url_pattern.format(name=voice)
        print(f"Baixando: {url}")
        r = requests.get(url)
        r.raise_for_status()
        content = io.BytesIO(r.content)
        data = torch.load(content, weights_only=True).numpy()
        voices[voice] = data
    with open(voices_file, "wb") as f:
        np.savez(f, **voices)
    print(f"Arquivo de vozes criado: {voices_file}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Iniciando download do modelo...")
    download_model(current_dir)
    print("Iniciando download das vozes...")
    download_all_voices(current_dir)
    print("Setup concluído.")
