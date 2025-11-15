# Conversation Analyzer

Download all the libraries using the requirements.txt file.
In addition to that, download FFMPEG library as Whisper model internally uses this to deocde the file into raw waveform data.

Then run the FASTAPI backend using 
```uvicorn app.main:app --reload```
Then access the web page using index.html and give permission to microphone and webcam to start interacting with the analyzer.
