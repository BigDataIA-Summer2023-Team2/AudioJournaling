from utils.generic import journal, llm
from utils.db_utils import schemas, crud, SessionLocal, models, schemas
from sqlalchemy.orm import Session
from cloudevents.http import CloudEvent
import functions_framework
from dotenv import load_dotenv
import os

table = os.getenv("table_name")
session = Session()
    
@functions_framework.cloud_event
def handle_audio_processing(cloud_event: CloudEvent, context):
    try:
        data = cloud_event.data

        event_id = cloud_event["id"]
        event_type = cloud_event["type"]

        bucket = data["bucket"]
        # name = data["name"]
        # metageneration = data["metageneration"]
        # timeCreated = data["timeCreated"]
        # updated = data["updated"]

        # Extract audio file name from Cloud Storage event
        # bucket_name = data["bucket"]
        file_name = data["name"]
        # audio = schemas.UserAudioMetadata(**data)
        # db_audio = crud.add_audio_metadata(db, audio)
        transcript, emotion= journal.process_user_audio(file_name)
        quote = llm.generate_suggestions(transcript, emotion)

        try:
            # Query the table and filter by name
            result = session.query(models.AudioDataMetadata.id).filter_by(name=file_name).first()

            if result:
                audio_id= result.id
        

            data_audio = {
                "audio_id": audio_id,
                "emotion": emotion,
                "transcript": transcript,
                "quote": quote
            }
            user_input = schemas.UserAudioDetails(**data_audio)
            
            crud.set_audio_details(session, user_input)
        except Exception as e:
            print(f"Error fetching ID by name: {e}")
            return None
        
    except Exception as e:
        # Log the error and return an error response
        print(f"Error processing audio: {str(e)}")
        return {"error": "An error occurred while processing the audio."}
