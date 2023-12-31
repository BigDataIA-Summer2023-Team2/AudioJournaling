from utils.db_utils import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from utils.generic import parse_timestamp, get_hashed_password
import bcrypt
from sqlalchemy.orm import validates, relationship
import re
from fastapi import HTTPException


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    audios = relationship('UserAudioMetadata', backref='user')

    def __init__(self, username, first_name, last_name, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.account_created = datetime.now()
        self.account_updated = datetime.now()
        self.set_password(password)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return "Print " + self.username

    def __iter__(self):
        for key in ["id", "first_name", "last_name", "username", "account_created", "account_updated"]:
            if key in ["account_created", "account_updated"]:
                yield key, parse_timestamp(getattr(self, key))
            else:
                yield key, getattr(self, key)
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise HTTPException('No username provided')

        if not isinstance(username, str):
            raise HTTPException('Username should be a string')

        if self.username:
            if self.username != username:
                raise HTTPException('Username update not allowed')
            else:
                return username

        # if User.query.filter(User.username == username).first():
        #     raise Exception('Username is already in use')

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, username):
            raise HTTPException(
                "Username doesn't have a valid email address")

        return username

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not first_name:
            raise Exception('first name can\'t be empty')

        if not isinstance(first_name, str):
            raise HTTPException('First name should be a string')

        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not last_name:
            raise HTTPException('last name can\'t be empty')

        if not isinstance(last_name, str):
            raise HTTPException('last name should be a string')

        return last_name

    def set_password(self, password):
        if not password:
            raise HTTPException('Password not provided')

        if not isinstance(password, str):
            raise HTTPException('password should be a string')

        if len(password) < 8 or len(password) > 50:
            raise HTTPException(
                'Password must be between 8 and 50 characters')
        self.password_hash = get_hashed_password(password).decode('utf-8')


class UserAudioMetadata(Base):
    __tablename__ = 'users_audio_metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_url = Column(String(500), unique=True, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now())
    user_id = Column(
        Integer, ForeignKey('users.id'), nullable=False)
    emotion = Column(String(100))
    transcript = Column(String(100000))
    quote = Column(String(100000))
    
    def __init__(self, file_url, user_id):
        self.file_url = file_url
        self.timestamp = datetime.now()
        self.user_id = user_id
        self.emotion = None

    def set_emotion(self, emotion):
        self.emotion = emotion

    def set_transcript(self, transcript):
        self.transcript = transcript

    @validates('file_url')
    def validate_name(self, key, file_url):
        if not file_url:
            raise HTTPException('name can\'t be empty')

        if not isinstance(file_url, str):
            raise HTTPException('File URL should be a string')
        return file_url

class AudioDataMetadata(Base):
    __tablename__ = 'audio_data_metadata'

    index = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(String(100), nullable=False)
    emotion = Column(String(100), nullable=False)
    source = Column(String(100), nullable=False)
    path = Column(String(500),unique = True, nullable=False)
    gcp_url = Column(String(500), nullable=False)
