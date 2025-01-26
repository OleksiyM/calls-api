FROM python:3.11.9-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main

RUN apt-get update && apt-get install -y wget unzip ffmpeg git build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install git+https://github.com/openai/whisper.git

# RUN pip install spacy
RUN pip install spacy==3.7.6 

RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8080

ENTRYPOINT ["python","start.py"] 
