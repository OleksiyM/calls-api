- [Backend | DEV Challenge XXI](#backend--dev-challenge-xxi)
    - [Description](#description)
        - [Your task](#your-task)
        - [Description of input data](#description-of-input-data)
    - [Requirements](#requirements)
        - [Format of presentation of results](#format-of-presentation-of-results)

# Backend | DEV Challenge XXI

[Link](https://app.devchallenge.it/challenges/backend-dev-challenge-xxi)  / Online Round

## Description

[Ministry of Foreign Affairs of Ukraine](https://mfa.gov.ua/en)  (MFA of Ukraine) is a central executive body whose
activities are directed and coordinated by the Cabinet of Ministers of Ukraine. The MFA of Ukraine is the main body in
the system of central executive authorities in formulating and ensuring the implementation of the state policy in the
field of foreign relations of Ukraine.

### Your task

The Ministry of Foreign Affairs needs to process and analyze a large volume of telephone conversations. The goal is to
create a structured dataset from audio recordings of these conversations, which can be used for future analysis and
insights. If a conversation mentions a person's name and location, the system should extract and populate these details
into the appropriate fields. Additionally, the system must categorize each conversation into one or more relevant
categories and determine the emotional tone of the conversation

### Description of input data

As a user, I want to have API service with exact endpoints:

**CRUD of Category**
Categories represent the topics of conversation. Each conversation may cover multiple topics simultaneously. The
conversation topics must be assigned correctly, as specialists will evaluate and assess the quality of the calls based
on these topics from their respective fields.

When adding or updating a category, it is necessary to check if the conversations still belong to this category.

**GET /category**  – Returns a list of all conversation topics.

```
[{ "id": "category_id_1", "title": "Visa and Passport Services", "points": ["Border crossing", "International documentation"]}]
```

**POST /category**  – Creates a new conversation topic.
Request:

```
{"title": "Topic Title", "points": ["Key Point 1", "Key Point 2"]}
```

Success Response (201 Created):

```
{"id": "new_category_id", "title": "Topic Title", "points": ["Key Point 1", "Key Point 2"]}
```

Error Response (422 Unprocessable Entity)

**PUT /category/{category_id}**  – Updates an existing conversation topic.

Request:

```
{"title": "New Topic Title", "points": ["New Key Point 1", "New Key Point 2"]}
```

Success Response (200 OK):

```
{ "id": "category_id", "title": "New Topic Title", "points": ["New Key Point 1", "New Key Point 2"] }
```

Error Response (422 Unprocessable Entity)

**DELETE /category/{category_id}**  – Deletes a conversation topic by the specified identifier.

Success Response (200 OK)

Error Response (404 Not Found)

Validation Rules:

- **title**  is required for POST, optional for PUT.
- **points**  must be an array of strings if provided.

**Call**

This API provides functionality for processing and analyzing audio calls. It allows users to submit audio files via a
URL, where the service will handle the download, transcription, and analysis of the content. The system extracts key
information such as the caller's name and location, determines the emotional tone of the conversation, and stores the
results. Users can retrieve detailed information about a specific call using its unique identifier. The API supports wav
and mp3 file formats and provides clear responses for successful operations as well as error conditions.

**POST /call**  – Creates a new call based on the provided audio file URL. Supported file formats are wav and mp3.

Request:

```
{"audio_url": "[http://example.com/audiofile.wav](http://example.com/audiofile.wav)"}
```

Success Response (200 OK):

```
{"id": "new_call_id"}
```

Error Response (422 Unprocessable Entity) if invalid audio file or URL.

**GET /call/{id}**  – Retrieves details of a call by the specified identifier. The emotional tone must be one of the
following values: Neutral, Positive, Negative, Angry. For the name and location fields: These are extracted from the
call if possible. If extraction is not feasible or the information is unavailable, the fields will be returned as null

Success Response (200 OK):

```
{  
  "id": "call_id",  
  "name": "Call Name",  
  "location": "Kyiv",  
  "emotional_tone": "Neutral",  
  "text": "Transcribed text",  
  "categories": ["Topic Title 1","Topic Title 2"]
}
```

Response (202 Accepted) if processing is not yet complete

## Requirements

1. By default, five conversation topics should be created: Visa and Passport Services, Diplomatic Inquiries, Travel
   Advisories, Consular Assistance, Trade and Economic Cooperation.
2. The system must be capable of operating without internet access (without relying on external services). File links
   can be sourced from a local network.
3. Calls conversation are conducted  **in English**.
4. In the README, please describe the corner cases that are covered.

### Format of presentation of results

Upload the source on the platform in  **one file archive**  with the name in the format **FileName.zip**.

☝️ Please note that the .git directory should not be present in the archive.

☝️ Please note that the name of the archive and file names inside the archive should not contain your first or last
name. The size of the solution archive should not exceed  **10 MB**.

**The archive should contain**

1. 'docker-compose' file in the root, which starts a server with the given endpoints on '/api' URI on port 8080,
   available from localhost as [http://localhost:8080/](http://localhost:8080/).
2. Ensure the Docker container name is unique using the format {you_id}_devchalenge_21.
3. README.md, where you wrote instructions on how to start service and tests and some thoughts about your choices during
   performing this task and the next steps to make your service better.
4. 