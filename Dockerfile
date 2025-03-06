FROM python:3.12-alpine@sha256:28b8a72c4e0704dd2048b79830e692e94ac2d43d30c914d54def6abf74448a4e

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN echo 'hadolint check meow'

CMD ["python", "main.py"]