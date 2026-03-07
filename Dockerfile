# syntax=docker/dockerfile:1

## ---- Build stage using uv's official image ----
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

## Install dependencies using uv (locked for reproducibility)
RUN uv sync --frozen --no-install-project --no-dev

## Copy the rest of the project
COPY . .

## Install the project itself
RUN uv sync --frozen --no-dev

## Exposed PORT
EXPOSE 8501

## Run the app via uv
CMD ["uv", "run", "streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]