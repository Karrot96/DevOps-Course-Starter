FROM python:3.8.5-slim-buster

WORKDIR ./app

RUN apt-get update && apt-get -y install \
    # Poetry install deps
    curl

EXPOSE 8000

ENV POETRY_VERSION=1.0.5
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"

COPY wsgi.py ./wsgi.py
COPY run.sh ./run.sh
RUN chmod +x ./run.sh
ENTRYPOINT [ "./run.sh" ]

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock

RUN poetry install --no-dev

COPY todo_app ./todo_app