FROM python:3.8-buster as base
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.2
RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false
WORKDIR /usr/src/app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install -v --no-dev


FROM base as dev
RUN poetry install -v
COPY . .

FROM base as prod
COPY . .


FROM prod as cli
COPY scripts/cli.sh /bin/cli

CMD bash
