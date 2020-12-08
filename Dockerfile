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
RUN poetry config.virtualenvs.create false --local && poetry install --no-dev --no-root
COPY todo_app ./todo_app

FROM base as development

EXPOSE 5000
ENTRYPOINT [ "./run.sh", "dev"]
RUN poetry install --no-root

FROM base as test

# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    apt-get update &&\
    apt-get install ./chrome.deb -y --fix-missing &&\
    rm ./chrome.deb
# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
echo "Installing chromium webdriver version ${LATEST}" &&\
curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
apt-get install unzip -y &&\
unzip ./chromedriver_linux64.zip

RUN poetry install --no-root
COPY . .
RUN chmod +x ./tests.sh

ENTRYPOINT [ "./tests.sh" ]