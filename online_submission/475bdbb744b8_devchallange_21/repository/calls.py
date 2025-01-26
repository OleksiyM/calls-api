import os

import aiohttp
import spacy
import whisper
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from textblob import TextBlob

from config.constants import ANGRY_KEYWORDS, UKRAINIAN_CITIES, COUNTRY, POSITIVE_THRESHOLD, NEGATIVE_THRESHOLD, \
    MSG_FAILED_DOWNLOAD, MSG_UNEXPECTED_ERROR
from entity.models import Call
from repository.categories import get_categories
from schemas.calls import CallCreate

# Initialize the Whisper model
model = whisper.load_model("base")

nlp = spacy.load("en_core_web_sm")

async def get_call_by_id(db: AsyncSession, call_id: int):
    """
    Function to retrieve a call by its ID.
    :param db: AsyncSession object for database operations.
    :param call_id: ID of the call to retrieve.
    :return: The call object if found, otherwise None.
    """
    
    stmt = select(Call).filter(Call.id == call_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_call(db: AsyncSession, call: CallCreate):
    """
    Function to create a new call.
    :param db: AsyncSession object for database operations.
    :param call: CallCreate object containing the call details.
    :return: The created call object.
    """

    # Set the temporary directory path
    temp_dir = "tmp"
    
    # Check if the tmp directory exists, and create it if it doesn't
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)  # Create the directory if it does not exist

    # Download the audio file asynchronously
    audio_url = call.audio_url
    file_name = os.path.basename(audio_url)
    
    # Create the audio_path using os.path.join for cross-platform compatibility
    audio_path = os.path.join(temp_dir, file_name)

    # Download and save the audio file locally
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(audio_url) as resp:
                if resp.status == 200:
                    with open(audio_path, "wb") as audio_file:
                        audio_file.write(await resp.read())
                else:
                    raise HTTPException(status_code=422, detail=MSG_FAILED_DOWNLOAD)
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=422, detail=f"{MSG_FAILED_DOWNLOAD}: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"{MSG_UNEXPECTED_ERROR}: {str(e)}")

    # Transcribe the audio using Whisper
    transcription_result = model.transcribe(audio_path)

    # Extract details from transcription (e.g., name, location, tone)
    text = transcription_result["text"]
    # print(text)
    
    name, location = extract_name_and_location(text)
    emotional_tone = detect_emotional_tone(text)

    # Detect the categories for the call based on the text
    categories = await detect_call_categories(db, text)
    print(categories)

    # Store call details
    db_call = Call(name=name, 
                   location=location, 
                   emotional_tone=emotional_tone, 
                   text=text, 
                   url=audio_url,
                   categories=categories)
    db.add(db_call)
    await db.commit()  # Await the commit
    await db.refresh(db_call)  # Await the refresh

    # Delete the temporary audio file after processing
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return db_call


def extract_name_and_location(text: str):
    """
    Function to extract name and location from the given text.
    :param text: The text to process.
    :return: A tuple containing the name and location extracted from the text.
    """

    # Initialize name and location
    name = "null"
    location = "null"
    
    doc = nlp(text)
    
    # Extract entities using spaCy NER
    for ent in doc.ents:
        if ent.label_ == "PERSON" and name == "null":  # Take the first occurrence of a person name
            name = ent.text
        elif ent.label_ == "GPE":  # Geopolitical Entity (for locations)
            if ent.text in UKRAINIAN_CITIES:
                location = ent.text  # If city found in list
            elif COUNTRY.lower() in ent.text.lower():
                location = COUNTRY  # For detecting Ukraine correctly
    
    # Fallback: If no city found, manually check for city in text
    if location == "null" or location == COUNTRY:
        for city in UKRAINIAN_CITIES:
            if city.lower() in text.lower():
                location = city
                break
    
    # Fallback: If no city but the text mentions Ukraine, append Ukraine
    if COUNTRY in text and COUNTRY.lower() not in location.lower():
        if location == "null":
            location = COUNTRY
        else:
            location = f"{location}, {COUNTRY}"
    
    return name, location


def detect_emotional_tone(text: str) -> str:
    """
    Function to detect the emotional tone in the given text.
    :param text: The text to analyze.
    :return: The emotional tone detected ("Positive", "Negative", "Neutral", "Angry").
    """

    # Normalize the text for case-insensitive matching
    text_lower = text.lower()
    
    # Check if any angry keywords are present in the text
    if any(keyword in text_lower for keyword in ANGRY_KEYWORDS):
        return "Angry"

    # Use TextBlob for sentiment analysis for other tones
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # Determine emotional tone based on polarity
    if polarity > POSITIVE_THRESHOLD:
        return "Positive"
    elif polarity < NEGATIVE_THRESHOLD:
        return "Negative"
    else:
        return "Neutral"


async def detect_call_categories_(db: AsyncSession, text: str) -> list[str]:
    """
    Function to detect the categories for the given call text.
    :param db: AsyncSession object for database operations.
    :param text: The text of the call.
    :return: A list of category titles that match the call text.
    """
    
    # Fetch all categories from the database
    categories = await get_categories(limit=100, offset=0, db=db)
    # Use a set to prevent duplicates
    detected_categories = set()
    # NER Analysis
    doc = nlp(text)  

    for category in categories:
        print(category.points)
        if any(keyword in text.lower() for keyword in category.points):
            # print("Detected: ", category.title)
            detected_categories.add(category.title)
    
    # Additional NER check
    for ent in doc.ents:
        if ent.text.lower() in category.points:
            detected_categories.add(category.title)

    return list(detected_categories) 


async def detect_call_categories(db: AsyncSession, text: str) -> list[str]:
    """
    Function to detect the categories for the given call text.
    :param db: AsyncSession object for database operations.
    :param text: The text of the call.
    :return: A list of category titles that match the call text.
    """
    
    # Fetch all categories from the database
    categories = await get_categories(limit=100, offset=0, db=db)
    
    # Use a set to prevent duplicates
    detected_categories = set()

    # Convert text to lowercase for case-insensitive comparison
    lower_text = text.lower()
    
    # Check for category points in the text
    for category in categories:
        for keyword in category.points:
            # Ensure the keyword comparison is case-insensitive
            if keyword.lower() in lower_text:
                # print(f"Detected keyword '{keyword}' in category '{category.title}'")
                detected_categories.add(category.title)

    # NER Analysis (using spaCy)
    doc = nlp(text)  
    
    # Additional NER check for named entities
    for ent in doc.ents:
        ent_text_lower = ent.text.lower()  # Ensure entity text is also lowercased
        for category in categories:
            if any(keyword.lower() in ent_text_lower for keyword in category.points):
                # print(f"Detected NER entity '{ent.text}' in category '{category.title}'")
                detected_categories.add(category.title)

    return list(detected_categories)