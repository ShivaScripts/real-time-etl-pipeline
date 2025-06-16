# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install kafka-python faker pyspark

# Copy your source code
COPY src/producer src/producer
COPY src/consumer src/consumer
COPY src/sparkk src/sparkk

# Expose any ports if needed (e.g. Spark UI)
EXPOSE 4040

# Default command: show help
CMD ["bash"]
