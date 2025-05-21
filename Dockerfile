FROM python:3.12-slim
WORKDIR /app
COPY synthesize.py voices_v1.bin kokoro_v1.onnx ./
RUN pip install --no-cache-dir soundfile==0.13.0 argparse==1.4.0 numpy==2.2.0 \
    https://files.pythonhosted.org/packages/fd/00/48311d88757b160634af7626324fe8a95cae186952bf25baad831381d50f/kokoro_onnx-0.4.9-py3-none-any.whl \
    && chmod +x synthesize.py \
    && rm -rf ~/.cache/pip \
    && mkdir -p /app/shared
ENTRYPOINT ["python3", "./synthesize.py"]