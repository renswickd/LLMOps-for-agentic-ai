FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Work directory inside the docker container
WORKDIR /app

# Install system dependancies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Project setup
RUN pip install --no-cache-dir -e .

EXPOSE 8501
EXPOSE 9999

CMD ["python", "app/main.py"]