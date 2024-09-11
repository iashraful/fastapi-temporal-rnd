FROM python:3.12.5-bullseye

RUN apt update && \
    apt install -y build-essential gcc g++ python3-dev python3-pip libffi-dev

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY . /app/

# Project initialization:
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
