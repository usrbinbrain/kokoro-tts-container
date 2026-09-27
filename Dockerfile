FROM python:3.12-slim
WORKDIR /app
COPY synthesize.py voices_v1.bin kokoro_v1.onnx ./
RUN pip install --no-cache-dir soundfile==0.13.0 argparse==1.4.0 numpy==2.2.0 \
    https://files.pythonhosted.org/packages/60/e1/a27e5a70a525a5ee1fd5357596f07b724d02ff317f134e86cb6e3d9db968/kokoro_onnx-0.6.1-py3-none-any.whl \
    && chmod +x synthesize.py \
    && rm -rf ~/.cache/pip \
    && mkdir -p /app/shared
ENTRYPOINT ["python3", "./synthesize.py"]