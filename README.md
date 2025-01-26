- [Calls API](#calls-api)
  - [Project Description](#project-description)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
    - [Backend Framework](#backend-framework)
    - [Database](#database)
    - [Audio Processing](#audio-processing)
    - [Natural Language Processing (NLP)](#natural-language-processing-nlp)
    - [Containerization](#containerization)
    - [Asynchronous Programming](#asynchronous-programming)
    - [Dependency Management](#dependency-management)
  - [Installation and Usage](#installation-and-usage)
    - [Running the App via Docker Compose](#running-the-app-via-docker-compose)
      - [Prerequisites](#prerequisites)
    - [Running the App Manually for the First Time](#running-the-app-manually-for-the-first-time)
      - [See detailes in the readme.md](#see-detailes-in-the-readmemd)
    - [Running the App Manually Next Time](#running-the-app-manually-next-time)
  - [Plans for Future Enhancements](#plans-for-future-enhancements)
  - [Contributing](#contributing)
  - [License](#license)

# Calls API

## Project Description

This project was developed as part of the [DevChallenge IT XXI](https://www.devchallenge.it/) Backend category. It
processes and analyzes telephone conversations to extract structured datasets for analysis. The system extracts details
such as names, locations,
emotional tones, and categorizes conversations based on content. It operates without internet dependency and supports
local file processing. Detailed task you can see in the [task.md](task.md)

## Features

- Submit audio files via a URL for processing.
- Extract key information, including names and locations mentioned in conversations.
- Determine the emotional tone of conversations.
- Categorize conversations into relevant groups.
- Support for multiple audio formats (e.g., WAV, MP3).
- RESTful API accessible through a user-friendly documentation interface.
- Local file handling and offline processing capabilities.

## Technologies Used

### Backend Framework

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard
  Python type hints.

### Database

- **PostgreSQL**: A powerful, open-source object-relational database system.
- **SQLAlchemy**: SQL toolkit and ORM for database interaction.
- **Alembic**: A lightweight database migration tool for SQLAlchemy.

### Audio Processing

- **Whisper**: OpenAI’s automatic speech recognition model, used for transcribing audio to text.
- **ffmpeg**: A multimedia framework for handling audio and video processing.

### Natural Language Processing (NLP)

- **SpaCy**: Used for extracting names and locations from transcriptions.
- **TextBlob**: Provides tools for text analysis, such as sentiment analysis.

### Containerization

- **Docker**: To containerize the application for consistent deployment across environments.
- **Docker Compose**: For defining and running multi-container Docker applications.

### Asynchronous Programming

- **aiohttp**: Used for asynchronous HTTP requests.

### Dependency Management

- **Poetry**: Python packaging and dependency management tool.

## Installation and Usage

### Running the App via Docker Compose

#### Prerequisites

- Docker Desktop installed on your machine.

Run the following commands in the app directory:

```bash
docker-compose up -d --build
```

After the first run, the database and additional resources (e.g., `whisper/base.pt`) will be set up. This may take some
time. To restart the server:

```bash
docker-compose down
```

```bash
docker-compose up -d
```

Access the API via the documentation interface at:

```
http://localhost:8080/docs#/
```

### Running the App Manually for the First Time

#### See detailes in the [readme.md](online_submission/475bdbb744b8_devchallange_21/readme.md)

Access the API at:

```
http://localhost:8080/docs#/
```

### Running the App Manually Next Time

From the app directory:

```bash
poetry shell
uvicorn main:app --port 8080 --reload
```

## Plans for Future Enhancements

- [ ] Add more detailed error handling and logging.
- [ ] Add support for more audio file formats.
- [ ] Improve the accuracy of name and location extraction.
- [ ] Enhance the emotional tone detection algorithm.
- [ ] Add more categories and improve category detection.
- [ ] Implement a web-based user interface for easier interaction with the API.

## Contributing

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

