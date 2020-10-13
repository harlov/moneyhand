FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.2

RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false

WORKDIR /usr/src/app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install -v
