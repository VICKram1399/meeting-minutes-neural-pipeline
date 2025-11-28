# Use an official Python runtime as a parent image
# 3.10 is a stable choice for AI libraries
FROM python:3.10-slim

# Set metadata
LABEL maintainer="Your Name"
LABEL description="Meeting Minutes Neural Pipeline API"

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# We need ffmpeg for audio processing and git/build-essential for some pip packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir keeps the image size smaller
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create necessary directories for data (if they don't exist)
RUN mkdir -p data/raw_audio data/processed_audio data/output_json logs

# Expose the port that FastAPI runs on
EXPOSE 8000

# Define the command to run the application
# host 0.0.0.0 makes it accessible from outside the container
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
