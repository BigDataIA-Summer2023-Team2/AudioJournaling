from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    cnf_password: str
    firstname: str
    lastname: str

class UserAuthentication(UserBase):
    password: str

class UserAudioMetadata(BaseModel):
    file_url: str
    user_id: int

class UserAudioHistory(BaseModel):
    start_date: datetime
    end_date: datetime
    user_id: int

class UserAudioEmotion(BaseModel):
    audio_id: int
    emotion: str

class DatasetAudio(BaseModel):
    audio_path: str

class UserAccessTokenValidation(BaseModel):
    access_token: str
