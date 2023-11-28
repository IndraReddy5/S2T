from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_DB_URL"))
database = client[os.getenv("DATABASE_NAME")]
user_collection = database.users
audio_ct_collection = database.audio_ct
audio_transcriptions_collection = database.audio_transcriptions
words_freq_collection = database.words_freq
user_words_freq_collection = database.user_words_freq
user_top_phrases_collection = database.user_top_phrases
similar_users_collection = database.similar_users
