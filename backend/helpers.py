from auth import *
from fastapi import UploadFile
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import whisper
import string
import warnings
import nltk

warnings.filterwarnings("ignore", category=UserWarning)
nltk.data.path.append('backend/nltk_data/')

async def save_audio_file(file: UploadFile, filename: str):
    contents = file.read()
    if not os.path.exists(f"audio_store/"):
        os.makedirs(f"audio_store/")
    with open(f"audio_store/{filename}", "wb") as f:
        f.write(contents)
    return {"message": "File saved"}

async def get_transcriptions(audio_file: str):
    model = whisper.load_model("model/base.pt", device="cpu")
    result = model.transcribe(
        f"audio_store/{audio_file}",
        initial_prompt="convert this into english",
    )
    lemmatizer = WordNetLemmatizer()
    phrases = []
    words = []
    filter_chars = set(stopwords.words('english') + list(string.punctuation))
    for seg in result["segments"]:
        phrases.append(seg["text"].strip())
    for word in result['text'].split():
        if word not in filter_chars:
            words.append(lemmatizer.lemmatize(word.lower().strip(string.punctuation)))
    return result['text'].strip(), phrases, words


async def get_top_phrases(transcriptions: List[str]):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

    # Encode sentences to get sentence embeddings
    sentence_embeddings = model.encode(transcriptions, convert_to_tensor=True)

    # Calculate cosine similarity matrix
    cosine_similarities = util.pytorch_cos_sim(sentence_embeddings, sentence_embeddings)

    # Find three most unique sentences
    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit_predict(cosine_similarities)

    unique_indices = [
        cluster[0] for cluster in kmeans.cluster_centers_.argsort()[:, -1:-2:-1]
    ]
    unique_phrases = [transcriptions[i] for i in unique_indices]

    return unique_phrases
