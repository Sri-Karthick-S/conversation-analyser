from fastapi import APIRouter, File, UploadFile, Form, Request
import tempfile, cv2, datetime, pandas as pd
from moviepy.editor import VideoFileClip
from deepface import DeepFace
import os
import logging

router = APIRouter(prefix="/api", tags=["Analyze"])
logger = logging.getLogger(__name__)

@router.post("/analyze_video/")
async def analyze_video(request: Request, file: UploadFile = File(...), question: str = Form("Unknown")):

    logger.info("🎤 Received request for question: %s", question)

    models = request.app.state.models  # ✅ Correct way
    whisper_model = models["whisper"]
    sentiment_model = models["sentiment"]
    emotion_model = models["emotion"]
    topic_model = models["topic"]
    
    # 1. Save video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_video:
        temp_video.write(await file.read())
        temp_video_path = temp_video.name

    # 2. Extract audio
    video = VideoFileClip(temp_video_path)
    audio_path = temp_video_path.replace(".webm", ".wav")
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)

    # 3. Transcribe
    logger.info("🧠 Starting transcription...")
    result = whisper_model.transcribe(audio_path)
    transcript = result.get("text", "").strip()
    logger.info("📝 Transcript: %s", transcript[:100] or "[Empty]")
    
    # 4. Sentiment & Emotion
    sentiment = sentiment_model(transcript)[0]["label"]
    text_emotion = emotion_model(transcript)[0]["label"]
    logger.info("✅ Analysis complete | Sentiment: %s | Emotion: %s", sentiment, text_emotion)
    

    # 5. Facial emotion detection
    cap = cv2.VideoCapture(temp_video_path)
    frame_count, face_emotions = 0, []
    while True:
        success, frame = cap.read()
        if not success: break
        if frame_count % 15 == 0:  # sample every 15 frames
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                face_emotions.append(result[0]['dominant_emotion'])
            except Exception:
                pass
        frame_count += 1
    cap.release()
    facial_emotion = max(set(face_emotions), key=face_emotions.count) if face_emotions else "Unknown"
    
    # 6. Topic Modeling
    keywords = topic_model.extract_keywords(
        transcript,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=5
    )
    main_topics = [kw[0] for kw in keywords]
    main_topic_name = ", ".join(main_topics)
    logger.info("📚 Extracted topics: %s", main_topic_name)


    # 7. Save log
    df = pd.DataFrame([{
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "transcript": transcript,
        "sentiment": sentiment,
        "text_emotion": text_emotion,
        "facial_emotion": facial_emotion,
        "topic": main_topic_name
    }])
    df.to_csv("video_session_log.csv", mode="a", header=not os.path.exists("video_session_log.csv"), index=False)

    return {
        "question": question,
        "transcript": transcript,
        "sentiment": sentiment,
        "text_emotion": text_emotion,       
        "facial_emotion": facial_emotion,
        "topic": main_topic_name
    }

@router.post("/analyze_audio/")
async def analyze_audio(
    request: Request,
    file: UploadFile = File(...),
    question: str = Form("Unknown Question")
):
    logger.info("🎤 Received request for question: %s", question)

    try:
        models = request.app.state.models  # ✅ Correct way
        whisper_model = models["whisper"]
        sentiment_model = models["sentiment"]
        emotion_model = models["emotion"]
    except Exception as e:
        logger.exception("❌ Error accessing models: %s", e)
        return {"error": "Model access failed."}

    # Step 1 — Save audio file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name
        logger.info("💾 Saved temporary audio file: %s", temp_audio_path)
    except Exception as e:
        logger.exception("❌ Failed to save audio: %s", e)
        return {"error": "Failed to save audio file."}

    # Step 2 — Transcribe
    try:
        logger.info("🧠 Starting transcription...")
        result = whisper_model.transcribe(temp_audio_path)
        transcript = result.get("text", "").strip()
        logger.info("📝 Transcript: %s", transcript[:100] or "[Empty]")
    except Exception as e:
        logger.exception("❌ Whisper transcription failed: %s", e)
        return {"error": "Transcription failed."}

    if not transcript:
        logger.warning("⚠️ No speech detected for question: %s", question)
        return {"question": question, "error": "No speech detected."}

    # Step 3 — Sentiment & Emotion
    try:
        sentiment = sentiment_model(transcript)[0]["label"]
        emotion = emotion_model(transcript)[0]["label"]
        logger.info("✅ Analysis complete | Sentiment: %s | Emotion: %s", sentiment, emotion)
    except Exception as e:
        logger.exception("❌ Text analysis failed: %s", e)
        return {"error": "Text analysis failed."}

    # Step 4 — Save to CSV
    try:
        df = pd.DataFrame([{
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "transcript": transcript,
            "sentiment": sentiment,
            "emotion": emotion
        }])
        df.to_csv(
            "conversation_log.csv",
            mode="a",
            header=not pd.io.common.file_exists("conversation_log.csv"),
            index=False
        )
        logger.info("📊 Logged results to conversation_log.csv")
    except Exception as e:
        logger.warning("⚠️ Could not save CSV log: %s", e)

    return {
        "question": question,
        "transcript": transcript,
        "sentiment": sentiment,
        "emotion": emotion
    }
