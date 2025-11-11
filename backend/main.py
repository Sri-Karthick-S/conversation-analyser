from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import tempfile
import datetime
import json

from models_loader import load_models

app = FastAPI(title="Conversational Emotion & Sentiment Analyzer")

# CORS setup (so frontend can call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models once at startup
whisper_model, sentiment_model, emotion_model = load_models()

@app.post("/analyze_audio/")
async def analyze_audio(file: UploadFile = File(...), granularity: str = Form("sentence")):
    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    # Step 1: Transcribe
    result = whisper_model.transcribe(temp_audio_path)
    segments = result["segments"]

    # Step 2: Group text (light granularity = sentence)
    all_text = " ".join([seg["text"] for seg in segments])
    sentences = [s.strip() for s in all_text.split(".") if s.strip()]

    # Step 3: Run models
    records = []
    for sent in sentences:
        sentiment = sentiment_model(sent)[0]["label"]
        emotion = emotion_model(sent)[0]["label"]

        records.append({
            "text": sent,
            "sentiment": sentiment,
            "emotion": emotion
        })

    # Step 4: Save to CSV
    df = pd.DataFrame(records)
    filename = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)

    # Step 5: Return JSON results
    return {"granularity": granularity, "results": records, "file": filename}
