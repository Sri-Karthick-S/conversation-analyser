from transformers import pipeline
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import whisper
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

def ensure_ffmpeg():
    """Ensure ffmpeg is available cross-platform."""
    ffmpeg_env_path = os.getenv("FFMPEG_PATH")

    # Use .env variable if provided
    if ffmpeg_env_path and ffmpeg_env_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + ffmpeg_env_path
        print(f"✅ Using FFmpeg from .env: {ffmpeg_env_path}")
        return

    # Check if ffmpeg is in PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"✅ FFmpeg found at: {ffmpeg_path}")
    else:
        print("❌ FFmpeg not found. Please install it and add to PATH.")
        raise RuntimeError("FFmpeg is required for Whisper but not found.")

def load_models():
    """Load Whisper, Sentiment, and Emotion models."""
    ensure_ffmpeg()

    print("🔄 Loading models (first time might take a few minutes)...")

    whisper_model = whisper.load_model("tiny")  # Smallest CPU model

    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="siebert/sentiment-roberta-large-english"
    )

    emotion_analyzer = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=False
    )

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    topic_model = KeyBERT(model=embedding_model)

    print("✅ All models loaded successfully.")
    return whisper_model, sentiment_analyzer, emotion_analyzer, topic_model
