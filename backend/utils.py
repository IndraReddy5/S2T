from helpers import *

# Retrieving user audio files url and transcription from db
async def get_audio_ct(username: str):
    audio_ct = audio_ct_collection.find({"username": username})
    return await audio_ct.to_list(length=await audio_ct_collection.count_documents({"username": username}))


# Retrieving top 20 words that are most frequently used by users from db
async def get_top_words():
    top_words = words_freq_collection.find({}).sort("frequency", -1)
    return await top_words.to_list(length=20)


# Retrieving user top phrases from db
async def get_user_top_phrases(username: str):
    top_phrases = user_top_phrases_collection.find_one({"username": username})
    tp = await top_phrases
    if tp:
        return UserTopPhrases(username=username, transcriptions=tp["transcriptions"])
    else:
        return UserTopPhrases(username=username, transcriptions=[])
    return await top_phrases


# Retrieving user words freq from db
async def get_user_words_freq(username: str, arg_length: int = 5):
    top_words = user_words_freq_collection.find({"username": username}).sort(
        "frequency", -1
    )
    if arg_length == all:
        return await top_words.to_list(
            length=await user_words_freq_collection.count_documents(
                {"username": username}
            )
        )
    return await top_words.to_list(length=arg_length)


# adding/modifying top phrases of user in db
async def add_top_phrases(username: str, audio_transcriptions: List[str] = []):
    top_phrases = await get_user_top_phrases(username)
    transcriptions = []
    if top_phrases != []:
        if top_phrases.transcriptions:
            transcriptions.extend(top_phrases.transcriptions)
    transcriptions.extend(audio_transcriptions)
    if len(transcriptions) > 3:
        top_phrases = await get_top_phrases(transcriptions)
    else:
        top_phrases = transcriptions
    await user_top_phrases_collection.update_one(
        {"username": username}, {"$set": {"transcriptions": top_phrases}}, upsert=True
    )
    return {"message": "Top phrases added"}


# adding/modifying top words of user in db
async def add_top_words(username: str, words: List[str] = []):
    for word in words:
        await user_words_freq_collection.update_one(
            {"username": username, "word": word},
            {"$inc": {"frequency": 1}},
            upsert=True,
        )
    return {"message": "Top words added"}


# adding/modifying words freq of user in db
async def add_words_freq(username: str, words: List[str] = []):
    for word in words:
        try:
            await words_freq_collection.update_one(
            {"word": word}, {"$inc": {"frequency": 1}}, upsert=True
        )
        except:
            raise HTTPException(status_code=500, detail="Internal server error")
    return {"message": "Words frequency added"}

# adding complete audio transcription to audio_ct collection
async def add_audio_ct(username: str, audio_file: str, audio_ct: str):
    try:
        await audio_ct_collection.insert_one(
            {
                "username": username,
                "audio_file": audio_file,
                "audio_ct": audio_ct.strip(),
            }
        )
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
    return {"message": "Audio complete transcription added"}


# adding/modifying audio transcriptions
async def add_audio_transcriptions(
    username: str, audio_file: str, audio_transcriptions: List[str]
):
    for audio_transcription in audio_transcriptions:
        try:
            await audio_transcriptions_collection.insert_one(
                {
                    "username": username,
                    "audio_file": audio_file,
                    "transcription": audio_transcription.strip(),
                }
            )
        except:
            raise HTTPException(status_code=500, detail="Internal server error")
    return {"message": "Audio transcriptions added"}


# Retrieving similar_users from db
async def get_similar_users(username: str):
    similar_users = await similar_users_collection.find_one({"username": username})
    return similar_users


# adding/modifying similar users of user in db
async def add_similar_users(username: str, similar_users: List[str]):
    await similar_users_collection.update_one(
        {"username": username}, {"$set": {"similar_users": similar_users}}, upsert=True
    )
