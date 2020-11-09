FROM python:3.8-buster as base
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.4
ENV PATH=${PATH}:/root/.poetry/bin

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -o /tmp/get-poetry.py && \
    python /tmp/get-poetry.py --version $POETRY_VERSION && \
    poetry config virtualenvs.create false
WORKDIR /usr/src/app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install -v --no-dev


FROM base as dev
ENV PYTHONPATH=/usr/src/app
RUN poetry install -v
COPY . .


FROM dev as tests
CMD ./scripts/test.sh

FROM base as prod
COPY . .


FROM prod as cli
COPY scripts/cli.sh /bin/cli


FROM prod as telegram_bot
COPY scripts/run_telegram_bot.sh /bin/run_telegram_bot

CMD bash
