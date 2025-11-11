from transformers import pipeline
import whisper

def load_models():
    whisper_model = whisper.load_model("tiny")
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    emotion_analyzer = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=False
    )
    return whisper_model, sentiment_analyzer, emotion_analyzer
