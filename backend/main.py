from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
import os
from utils import *

app = FastAPI()

origins = [
    os.getenv("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="audio_store"), name="static")

@app.post("/create_user")
async def create_new_user(user: User):
    await create_user(user)
    return {"message": "User created"}


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if await authenticate_user(form_data.username, form_data.password):
        return await create_token(form_data.username)
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.get("/get_users", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_user)):
    x = user_collection.find({})
    return await x.to_list(length=await user_collection.count_documents({}))


@app.get("/get_token", response_model=Token)
async def get_token(new_token: User = Depends(get_new_token)):
    return new_token


@app.get("/top_words", response_model=List[WordsFreq])
async def get_top_words_freq(current_user: User = Depends(get_current_user)):
    if current_user:
        return await get_top_words()


@app.get("/{username}/top_words", response_model=List[UserWordsFreq])
async def get_user_top_words(
    username: str, current_user: User = Depends(get_current_user)
):
    if current_user.username == username:
        return await get_user_words_freq(username)
    raise HTTPException(status_code=403, detail=f"You can't see {username} top words")


@app.post("/{username}/add_words")
async def add_user_words(
    username: str, words: List[str] = [], current_user: User = Depends(get_current_user)
):
    if current_user.username == username:
        return await add_top_words(username, words)
    raise HTTPException(
        status_code=403, detail=f"You can't add words to {username} top words"
    )


@app.post("/{username}/add_top_phrases")
async def add_user_top_phrases(
    username: str,
    audio_transcriptions: List[str] = [],
    current_user: User = Depends(get_current_user),
):
    if current_user.username == username:
        return await add_top_phrases(username, audio_transcriptions)
    raise HTTPException(
        status_code=403, detail=f"You can't add top phrases to {username} top phrases"
    )


@app.post("/get_transcription/")
async def get_transcriptions_from_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    print(file)
    str_filename = dt.now().strftime("%Y_%m_%d_%H_%M_%S_") + file.filename.replace(" ", "_")
    await save_audio_file(file.file, str_filename)
    transcription, phrases, words = await get_transcriptions(str_filename)
    await add_audio_ct(current_user.username, str_filename, transcription)
    await add_audio_transcriptions(current_user.username, str_filename, phrases)
    await add_words_freq(current_user.username, words)
    await add_top_words(current_user.username, words)
    await add_top_phrases(current_user.username, phrases)
    return {"transcription": transcription, "phrases": phrases, "words": words, "audio_file": str_filename}


@app.get("/{username}/get_transcriptions", response_model=List[AudioCT])
async def get_transcriptions_from_db(username: str, current_user: User = Depends(get_current_user)):
    if current_user.username == username:
        return await get_audio_ct(username)
    raise HTTPException(
        status_code=403, detail=f"You can't get transcriptions from {username}"
    )
