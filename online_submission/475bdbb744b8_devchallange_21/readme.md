- [Calls API](#calls-api)
  - [Running app via Docker-compose](#running-app-via-docker-compose)
  - [Running app manually for the first time](#running-app-manually-for-the-first-time)
  - [Running manually next time](#running-manually-next-time)

# Calls API

## Running app via Docker-compose

**Prereq:**

- Docker Desktop

Run the following command in the app directory:

```bash
docker-compose up -d --build
```

After first run database will be created and some additional files like `whisper/base.pt`, may download, it takes some time.

You can wait couple of minutes and may be restart server with the commands:

```bash
docker-compose down
```

```bash
docker-compose up -d
```
or via Docker Desktop GUI interface

You can then interact with the API via a simple Doc GUI from your browser:

`http://localhost:8080/docs#/`

or via `curl` or other similar tools

**If Docker Compose containers aren't running, you can start the app manually.**

## Running app manually for the first time

**Prerequisites:**

- Docker Desktop
- Python 3.10 or above
- git command line (see below for details)
- ffmpeg (see below for details)

Make edit in the file `config/constants.py` like below (uncomment first line and comment second line):

```python
DB_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres' # run as unicorn web server 
# DB_URL = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres' # run in docker-compose
```

1. **Install and run poetry and activate the virtual environment.**

Run the following commands in the app directory:

```bash
pip install poetry
```

```bash
poetry install --no-root
```

```bash
poetry shell
```

2. **Install ffmpeg and git.**

You can install them manually from the links below:

- [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- [https://git-scm.com/downloads](https://git-scm.com/downloads)

Alternatively, run the following command (example for Linux debian-based):

```bash
apt-get update && apt-get install -y wget unzip ffmpeg git build-essential && rm -rf /var/lib/apt/lists/*
```

3. **Install packages:**

```bash
pip install git+https://github.com/openai/whisper.git
```

```bash
pip install spacy==3.7.6
```

```bash
python -m spacy download en_core_web_sm
```

4. **Run PostgreSQL:**

```bash
docker pull postgres:16
```

```bash
docker run --name calls-api-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:16
```

5. **Create database:**

```bash
alembic upgrade head
```

6. **Start app:**

```bash
uvicorn main:app --port 8080 --reload
```

You can then interact with the API via a simple Doc GUI from your browser:

```
http://localhost:8080/docs#/
```


## Running manually next time

From the app directory, run the following commands:

```bash
poetry shell
```

```bash
uvicorn main:app --port 8080 --reload
```

You can then interact with the API via a simple Doc GUI from your browser:

```
http://localhost:8080/docs#/
```
