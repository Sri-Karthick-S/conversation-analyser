let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusDiv = document.getElementById("status");

startBtn.onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);

  audioChunks = [];
  mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

  mediaRecorder.start();
  statusDiv.textContent = "Status: Recording...";
  startBtn.disabled = true;
  stopBtn.disabled = false;
};

stopBtn.onclick = async () => {
  mediaRecorder.stop();
  statusDiv.textContent = "Status: Processing...";
  startBtn.disabled = false;
  stopBtn.disabled = true;

  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append("file", blob, "audio.wav");

    const response = await fetch("http://127.0.0.1:8000/analyze_audio/", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    statusDiv.textContent = "Status: Analysis complete ✅";

    // Display results in table
    const tbody = document.querySelector("#results tbody");
    tbody.innerHTML = "";
    data.results.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${row.text}</td>
        <td>${row.sentiment}</td>
        <td>${row.emotion}</td>
      `;
      tbody.appendChild(tr);
    });
  };
};
