# conversation-analyser
Application to detect the emotions and sentiments over the conversation

## Setup
Create and activate the virtual environment (For windows):
```
python -m venv venv
venv\Scripts\activate
```

Install backend dependencies:
```
cd backend
pip install -r requirements.txt
```

Verify installation:
```
pip show fastapi transformers torch openai-whisper
```

Run the backend server:
```
uvicorn main:app --reload
```


