from utils.db_utils import SessionLocal, crud, schemas, models, engine
from utils.generic import decode_token, get_audio_transcript
from utils.gcp_utils import bucket
from utils.pinecone_utils import get_similar_audios
import os
import uuid
from datetime import datetime, timedelta
from utils.pinecone_utils import get_similar_audios
from utils.generic.llm import generate_suggestions
import requests
import json
import os

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://api:8095")

headers = {'Content-Type': 'application/json'}

models.Base.metadata.create_all(bind=engine)

def create_user(username, password, cnf_password, firstname, lastname):
    url = f"{BACKEND_API_URL}/api/v1/user"
    payload = {
        "username": username,
        "password": password,
        "cnf_password": cnf_password,
        "firstname": firstname,
        "lastname": lastname
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("username")
    else:
        return False, response.json().get("detail")

def authenticate_user(username, password):
    url = f"{BACKEND_API_URL}/api/v1/user/authenticate"
    payload  = {
        "username": username,
        "password": password
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("auth_token")
    else:
        return False, response.json().get("detail")

def validate_access_token(access_token):
    url = f"{BACKEND_API_URL}/api/v1/user/access_token"
    if not access_token:
        access_token = ""
    payload  = {
        "access_token": access_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("GET", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("username")
    else:
        return False, response.json().get("detail")

def create_new_audio(audio_file_name, access_token):
    url = f"{BACKEND_API_URL}/api/v1/user/journal/create"
    if not access_token:
        access_token = ""
    payload  = {
        "access_token": access_token,
    }
    files = {
        "audio_file": (f'{audio_file_name}', open(f'{audio_file_name}', 'rb'), 'audio/wav'),
    }
    response = requests.request("POST", url, data=payload, files=files)
    if response.status_code == 200:
        return True, response.json().get("quote")
    else:
        return False, response.json().get("detail")

def fetch_journal_history(access_token, start_date=datetime.now() - timedelta(5), end_date = datetime.now()):
    db = SessionLocal()
    decoded_info = decode_token(access_token)
    data = {
        "start_date": start_date,
        "end_date" : end_date,
        "user_id": decoded_info.get("user_id")
    }
    user_input = schemas.UserAudioHistory(**data)
    return crud.get_journal_history(db, user_input)

def fetch_file_gcs(file_url):
    file_name = bucket.download_as_file(file_url)
    return file_name

def process_user_audio(file_url):
    local_file_name = fetch_file_gcs(file_url)
    transcript = get_audio_transcript(local_file_name)
    audio_ids = get_similar_audios(local_file_name)
    db = SessionLocal()
    data = {
        "audio_path": audio_ids[0] 
    }
    user_input = schemas.DatasetAudio(**data)
    emotion = crud.get_emotion_audio_data(db, user_input)
    return transcript, emotion

def get_user_emotions(access_token, start_date=datetime.now() - timedelta(7), end_date=datetime.now()):
    db = SessionLocal()
    decoded_info = decode_token(access_token)
    data = {
        "start_date": start_date,
        "end_date" : end_date,
        "user_id": decoded_info.get("user_id")
    }
    user_input = schemas.UserAudioHistory(**data)
    emotions = crud.get_user_emotions(db, user_input)
    return emotions

# def generate_suggestion(audio_file, emotion):
#     audio_transcript = get_audio_transcript(audio_file)

# create_user("ashritha@gmail.com", "ashritha", "ashritha", "ashritha", "ashritha")
# jwt_token = authenticate_user("ashritha@gmail.com", "ashritha")[1]
# print(validate_access_token(jwt_token))
# result = create_new_audio("/Users/sayalidalvi/ashritha/Project_old/audio_journaling/archive/Actor_01/03-01-04-02-01-01-01.wav", jwt_token)
# print(result)
# from datetime import datetime, timedelta
# audio_history = fetch_journal_history(jwt_token, datetime.now() - timedelta(1),datetime.now())
# fetch_file_gcs(audio_history[13]['file_url'])
# result = get_user_emotions(jwt_token)
# print(result)
# path='/Users/rishabhindoria/Documents/GitHub/AudioJournaling/airflow/dags/bucketdata1001_DFA_ANG_XX.wav'
# print(get_similar_audios(path))
