FROM python:3.8.5-slim-buster as base

WORKDIR ./app

RUN apt-get update && apt-get -y install \
    # Poetry install deps
    curl

ENV POETRY_VERSION=1.0.5
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"

COPY run.sh ./run.sh
RUN chmod +x ./run.sh

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry config virtualenvs.create false

FROM base as production

EXPOSE 8000
ENTRYPOINT [ "./run.sh", "prod"]
RUN poetry install --no-dev --no-root
COPY todo_app ./todo_app

FROM base as development

EXPOSE 5000
ENTRYPOINT [ "./run.sh", "dev"]
RUN poetry install --no-root

