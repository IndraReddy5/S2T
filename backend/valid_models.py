from typing_extensions import Annotated
from pydantic import BaseModel, Field, EmailStr, StringConstraints
from typing import List


class User(BaseModel):
    username: str = Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=3, max_length=20)
    ]
    email: EmailStr = Field(..., alias="email")
    password: str

    class Config:
        json_scheme_extra = {
            "example": {
                "username": "username",
                "email": "test@s2t.in",
                "password": "s2t@test123",
            }
        }


class UserResponse(BaseModel):
    username: str = Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=3, max_length=20)
    ]
    email: EmailStr = Field(..., alias="email")

    class Config:
        json_scheme_extra = {
            "example": {
                "username": "jon",
                "email": "jon@fakegmail.com",
            }
        }


class AudioTranscriptions(BaseModel):
    username: str = Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=3, max_length=20)
    ]
    audio_file: str = Field(..., alias="audio_file")
    transcription: str = Field(..., alias="text")

    class Config:
        json_scheme_extra = {
            "example": {
                "username": "username",
                "audio_file": "21_01_2021_12_00_00.wav",
                "transcription": "hello, this is a test message",
            }
        }


class WordsFreq(BaseModel):
    word: str
    frequency: int

    class Config:
        json_scheme_extra = {
            "example": {
                "word": "hello",
                "frequency": 1,
            }
        }


class UserWordsFreq(BaseModel):
    username: str = Field(..., alias="username")
    word: str
    frequency: int

    class Config:
        json_scheme_extra = {
            "example": {
                "username": "username",
                "word": "hello",
                "frequency": 1,
            }
        }

class UserTopPhrases(BaseModel):
    username: str = Field(..., alias="username")
    transcriptions: List[str]


class AudioCT(BaseModel):
    username: str = Field(..., alias="username")
    audio_file: str = Field(..., alias="audio_file")
    transcription: str = Field(..., alias="audio_ct")


class SimilarUsers(BaseModel):
    username: str = Field(..., alias="username")
    similar_users: List[str]

