FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add whitenoise
RUN pip install --no-cache-dir whitenoise

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/media

EXPOSE 8000

CMD ["/app/start.sh"]
