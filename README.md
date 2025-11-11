# 🚀 Conversation Analyzer — Setup & Run Instructions

## 🧱 1️⃣ Prerequisites

Make sure the system has:

* **Python 3.10+**
* **Git** (for cloning or pulling code)
* **FFmpeg** (required by `moviepy` for audio extraction)

### Install FFmpeg:

```bash
# Windows
choco install ffmpeg
```

---

## ⚙️ 2️⃣ Clone or Copy the Repository

If your project is in GitHub:

```bash
git clone https://github.com/<your-repo>/conversation-analyser.git
cd conversation-analyser
```

Otherwise, copy the folder manually and navigate to the backend:

```bash
cd conversation-analyser/backend
```

---

## 🧩 3️⃣ Create and Activate a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows PowerShell:**

```bash
\venv\Scripts\Activate
```

---

## 📦 4️⃣ Install Dependencies

If you already exported your environment (recommended):

```bash
pip install -r requirements.txt
```

## ▶️ 6️⃣ Run the FastAPI Backend

From the backend directory:

```bash
uvicorn app.main:app --reload
```

If it's under a subfolder like `conversation-analyser/backend`:

```bash
cd backend
uvicorn app.main:app --reload
```

### Expected Logs:

```
🚀 Starting Conversation Analyzer Backend...
✅ All models loaded successfully in 19.84 seconds.
🏁 Backend fully ready to use in 19.92 seconds.
```

---

## 🌐 7️⃣ Open the Frontend

Open your HTML file directly in a browser:

```
conversation-analyser/frontend/index.html
```

You should see:

* The camera and microphone preview.
* Start/Stop buttons.
* Table for displaying results.

---

## 📡 8️⃣ Confirm the API Works

When you click **Start → Stop**, it will send a POST request to:

```
http://127.0.0.1:8000/api/analyze_video/
```

In the FastAPI console, you’ll see logs like:

```
🎥 Received video for question: Tell me about yourself.
🧠 Starting transcription...
✅ Analysis complete | Sentiment: Positive | Emotion: Joy
📚 Extracted topics: career growth, learning, motivation
```

---

## 🧾 9️⃣ Output Logs

* Logs are stored in:

  ```bash
  backend/logs/server.log
  ```

* Transcripts and analysis results are saved in:

  ```bash
  backend/video_session_log.csv
  ```

---

## 🧰 10️⃣ Common Fixes

| Issue                                       | Fix                                                               |
| ------------------------------------------- | ----------------------------------------------------------------- |
| `ImportError: No module named 'tf_keras'`   | `pip install tf-keras` or downgrade TensorFlow to `2.15.0`        |
| `moviepy.audio.io.ffmpeg_audiowriter` error | Ensure `ffmpeg` is installed and in PATH                          |
| Slow startup                                | Whisper & transformers are large — cached after first run         |
| `ERR_CONNECTION_REFUSED`                    | Ensure `uvicorn` is running and backend port `8000` is accessible |
| Permission issues (Mac/Linux)               | Run `chmod +x venv/bin/activate`                                  |

---

## 💾 11️⃣ Export the Working Environment

Once everything works smoothly:

```bash
pip freeze > requirements.txt
```

Now, anyone can replicate your setup with:

```bash
pip install -r requirements.txt
```

---

## ✅ Final Checklist

* [ ] FastAPI server running on port 8000
* [ ] Frontend connected and sending requests
* [ ] `video_session_log.csv` updating after each recording
* [ ] Backend startup time logged correctly

---

📘 **Optional:** Add this README.md to your GitHub repo for easy onboarding!
