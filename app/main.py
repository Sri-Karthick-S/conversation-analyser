import logging
import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.loaders import load_models
from app.routes import analyze, logs

# ========== SETUP LOGGING ==========
LOG_FILE = "server.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join("logs", LOG_FILE), mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("🚀 Starting Conversation Analyzer Backend...")

# ========== FASTAPI APP ==========
app = FastAPI(title="Conversational Emotion & Sentiment Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== MODEL LOADING WITH TIMING ==========
start_time = time.time()

try:
    whisper_model, sentiment_model, emotion_model, topic_model = load_models()
    load_time = time.time() - start_time
    logger.info(f"✅ All models loaded successfully in {load_time:.2f} seconds.")
except Exception as e:
    logger.exception("❌ Model loading failed: %s", e)
    raise

app.state.models = {
    "whisper": whisper_model,
    "sentiment": sentiment_model,
    "emotion": emotion_model,
    "topic": topic_model
}

# ========== ROUTES ==========
app.include_router(analyze.router)
app.include_router(logs.router)

logger.info("✅ API routes registered successfully.")
logger.info(f"🏁 Backend fully ready to use in {time.time() - start_time:.2f} seconds.")
