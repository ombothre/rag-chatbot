FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY . .

RUN uv sync

EXPOSE 8000

CMD [".venv/bin/python3", "api.py"]
