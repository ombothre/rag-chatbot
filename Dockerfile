FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

# Copy project files
COPY . .

RUN uv sync --system

# Expose port used in api.py
EXPOSE 8000

# Start the backend using python3 api.py
CMD ["python3", "api.py"]
