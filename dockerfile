# Use official Python 3.10 image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8080

# Run Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
