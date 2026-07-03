FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -Lo /usr/local/bin/ttyd https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 \
    && chmod +x /usr/local/bin/ttyd

WORKDIR /app

COPY . /app

EXPOSE 10000

ENV TERM=xterm-256color

CMD ["ttyd", "-p", "10000", "-W", "python", "src/tetris.py"]