# Use official Python 3.10 image
FROM python:3.10-slim

# Set environment variables (prevents Python from writing .pyc files and enables buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (optional: for Pillow/OpenCV etc., depending on your model)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask default port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
