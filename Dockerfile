# Use the official Python 3.11 full version image
FROM python:3.11-slim

# Set environment variables for Poetry
ENV POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies and Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies using Poetry
RUN poetry install --no-root

# Expose port 4999
EXPOSE 4999

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "4999"]