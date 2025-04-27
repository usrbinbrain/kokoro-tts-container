FROM python:3.12-slim
WORKDIR /app
COPY synthesize.py voices_v1.bin kokoro_v1.onnx ./
RUN pip install --no-cache-dir soundfile==0.13.0 argparse==1.4.0 numpy==2.2.0 \
    https://files.pythonhosted.org/packages/cd/ef/df373e151af2086379804974b03c1b053874655d3432302006d75c6be0cf/kokoro_onnx-0.4.5-py3-none-any.whl \
    && chmod +x synthesize.py \
    && rm -rf ~/.cache/pip \
    && mkdir -p /app/shared
ENTRYPOINT ["python3", "./synthesize.py"]