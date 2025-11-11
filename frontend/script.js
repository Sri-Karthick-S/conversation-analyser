// // === CONFIGURATION ===
// const questions = [
//   "Tell me about yourself.",
//   "What challenges have you faced recently?",
//   "What motivates you to perform well?",
//   "Describe a time you learned something new."
// ];

// let currentQuestion = 0;
// let mediaRecorder;
// let audioChunks = [];
// let stream;
// let audioContext, analyser, source, dataArray;
// let isRecording = false;

// const questionBox = document.getElementById("questionBox");
// const startBtn = document.getElementById("startBtn");
// const stopBtn = document.getElementById("stopBtn");
// const statusDiv = document.getElementById("status");

// // === MIC INDICATOR ELEMENT ===
// const micIndicator = document.createElement("div");
// micIndicator.style.width = "250px";
// micIndicator.style.height = "14px";
// micIndicator.style.background = "#222";
// micIndicator.style.margin = "10px 0";
// micIndicator.style.borderRadius = "6px";
// micIndicator.style.overflow = "hidden";
// const micLevel = document.createElement("div");
// micLevel.style.height = "100%";
// micLevel.style.width = "0%";
// micLevel.style.background = "#333";
// micIndicator.appendChild(micLevel);
// statusDiv.parentElement.insertBefore(micIndicator, statusDiv.nextSibling);

// // === INIT MICROPHONE ON PAGE LOAD ===
// window.addEventListener("DOMContentLoaded", async () => {
//   await initMic();
//   displayQuestion();
//   statusDiv.textContent = "🎧 Microphone ready. Click 'Start Recording' when ready.";
// });

// // === INITIALIZE MICROPHONE ===
// async function initMic() {
//   try {
//     stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//     audioContext = new AudioContext();
//     source = audioContext.createMediaStreamSource(stream);
//     analyser = audioContext.createAnalyser();
//     analyser.fftSize = 2048;
//     source.connect(analyser);
//     dataArray = new Uint8Array(analyser.frequencyBinCount);
//     console.log("✅ Microphone access granted.");
//   } catch (err) {
//     console.error("Microphone access denied:", err);
//     statusDiv.textContent = "❌ Please allow microphone access to continue.";
//   }
// }

// // === DISPLAY CURRENT QUESTION ===
// function displayQuestion() {
//   if (currentQuestion >= questions.length) {
//     questionBox.textContent = "🎉 All questions completed!";
//     startBtn.disabled = true;
//     stopBtn.disabled = true;
//     statusDiv.textContent = "Interview finished.";
//     return;
//   }

//   questionBox.textContent = `Question ${currentQuestion + 1}: ${questions[currentQuestion]}`;
//   statusDiv.textContent = "🎤 Ready to record your answer.";
// }

// // === START RECORDING ===
// async function startRecording() {
//   if (isRecording) return;

//   audioChunks = [];
//   mediaRecorder = new MediaRecorder(stream);
//   mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
//   mediaRecorder.onstop = onRecordingStop;

//   mediaRecorder.start();
//   isRecording = true;
//   visualizeMic();
//   statusDiv.textContent = "🔴 Recording... Click 'Stop Recording' when you finish.";
//   startBtn.disabled = true;
//   stopBtn.disabled = false;
// }

// // === STOP RECORDING ===
// function stopRecording() {
//   if (!isRecording) return;
//   mediaRecorder.stop();
//   isRecording = false;
//   statusDiv.textContent = "⏳ Processing...";
//   micLevel.style.width = "0%";
//   micLevel.style.background = "#333";
//   startBtn.disabled = false;
//   stopBtn.disabled = true;
// }

// // === HANDLE RECORDING STOP ===
// async function onRecordingStop() {
//   const blob = new Blob(audioChunks, { type: "audio/wav" });
//   const question = questions[currentQuestion];

//   const formData = new FormData();
//   formData.append("file", blob, "audio.wav");
//   formData.append("question", question);

//   try {
//     const response = await fetch("http://127.0.0.1:8000/api/analyze_audio/", {
//       method: "POST",
//       body: formData,
//     });

//     const data = await response.json();
//     if (data.error) {
//       statusDiv.textContent = "❌ " + data.error;
//     } else {
//       displayResult(data, blob);
//       statusDiv.textContent = "✅ Analysis complete.";
//       currentQuestion++;
//       setTimeout(displayQuestion, 1500);
//     }
//   } catch (error) {
//     console.error("Upload failed:", error);
//     statusDiv.textContent = "❌ Upload or analysis failed.";
//   }
// }

// // === DISPLAY RESULTS IN TABLE ===
// function displayResult(data, blob) {
//   const tbody = document.querySelector("#results tbody");
//   const tr = document.createElement("tr");
//   const audioURL = URL.createObjectURL(blob);

//   tr.innerHTML = `
//     <td>${data.question}</td>
//     <td>${data.transcript || "No transcript"}</td>
//     <td>${data.sentiment || "-"}</td>
//     <td>${data.emotion || "-"}</td>
//   `;

//   const replayCell = document.createElement("td");
//   const replayBtn = document.createElement("button");
//   replayBtn.textContent = "▶ Replay";
//   replayBtn.style.padding = "4px 10px";
//   replayBtn.onclick = () => new Audio(audioURL).play();
//   replayCell.appendChild(replayBtn);
//   tr.appendChild(replayCell);

//   tbody.appendChild(tr);
// }

// // === MIC VISUALIZER ===
// function visualizeMic() {
//   if (!audioContext || !analyser) return;

//   const draw = () => {
//     if (!isRecording) {
//       micLevel.style.width = "0%";
//       micLevel.style.background = "#333";
//       return;
//     }

//     analyser.getByteTimeDomainData(dataArray);
//     const amplitude = Math.max(...dataArray);
//     const loudness = Math.min(100, ((amplitude - 128) / 128) * 100);

//     micLevel.style.width = `${Math.abs(loudness)}%`;
//     micLevel.style.background =
//       amplitude > 145
//         ? "linear-gradient(90deg, #0f0, #ff0)"
//         : "#333";

//     requestAnimationFrame(draw);
//   };

//   draw();
// }

// // === BUTTON HANDLERS ===
// startBtn.onclick = startRecording;
// stopBtn.onclick = stopRecording;

const questions = [
  "Tell me about yourself.",
  "What motivates you to perform well?",
];
let currentQuestion = 0;
let recorder, chunks = [], stream;

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusDiv = document.getElementById("status");
const video = document.getElementById("preview");

async function init() {
  stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
  video.srcObject = stream;
  video.play();
  statusDiv.textContent = "Ready to record video and audio.";
}
init();

startBtn.onclick = () => {
  chunks = [];
  recorder = new MediaRecorder(stream, { mimeType: "video/webm" });
  recorder.ondataavailable = e => chunks.push(e.data);
  recorder.onstop = onStop;
  recorder.start();
  startBtn.disabled = true;
  stopBtn.disabled = false;
  statusDiv.textContent = "Recording...";
};

stopBtn.onclick = () => {
  recorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
  statusDiv.textContent = "Processing...";
};

async function onStop() {
  const blob = new Blob(chunks, { type: "video/webm" });
  const formData = new FormData();
  formData.append("file", blob, "video.webm");
  formData.append("question", questions[currentQuestion]);

  const res = await fetch("http://127.0.0.1:8000/api/analyze_video/", { method: "POST", body: formData });
  const data = await res.json();
  display(data);

  currentQuestion++;
  if (currentQuestion < questions.length) {
    statusDiv.textContent = "Next question ready.";
  } else {
    statusDiv.textContent = "All questions done!";
  }
}

function display(data) {
  const tbody = document.querySelector("#results tbody");
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td>${data.question}</td>
    <td>${data.transcript}</td>
    <td>${data.sentiment}</td>
    <td>${data.text_emotion}</td>
    <td>${data.facial_emotion}</td>
  `;
  tbody.appendChild(tr);
}
