# from utils.db_utils import Base
# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from datetime import datetime
# from utils.generic import parse_timestamp, get_hashed_password
# import bcrypt
# from sqlalchemy.orm import validates, relationship
# import re


# class AudioDatasetMetadata(Base):
#     __tablename__ = 'audio_data_metadata'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     emotion = Column(String(100), unique=True, nullable=False)
#     path = Column(String(100), unique=True, nullable=False)
#     gender = Column(String(100), nullable=False)
