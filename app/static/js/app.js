(() => {
  const btnRecord = document.getElementById('btnRecord');
  const btnStop = document.getElementById('btnStop');
  const btnSpeak = document.getElementById('btnSpeak');
  const statusEl = document.getElementById('status'); // optional if present
  const transcriptEl = document.getElementById('transcript');
  const responseEl = document.getElementById('responseText');
  const audioEl = document.getElementById('audioPlayer');

  let mediaRecorder = null;
  let chunks = [];

  function setStatus(t){ if (statusEl) statusEl.textContent = t; }

  // Recording flow
  async function startRecording(){
    setStatus("Requesting mic…");
    if (btnRecord) btnRecord.disabled = true;
    if (btnStop) btnStop.disabled = true;
    try{
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';
      mediaRecorder = new MediaRecorder(stream, { mimeType });

      chunks = [];
      mediaRecorder.ondataavailable = e => { if (e.data.size) chunks.push(e.data); };
      mediaRecorder.onstart = () => { setStatus("Recording…"); if (btnStop) btnStop.disabled = false; };
      mediaRecorder.onstop = async () => {
        setStatus("Processing…");
        if (btnStop) btnStop.disabled = true;
        try{
          const blob = new Blob(chunks, { type: mimeType });
          const fd = new FormData();
          fd.append('audio', blob, 'recording.webm');
          const res = await fetch('/api/process', { method:'POST', body: fd });
          if (!res.ok){
            const txt = await res.text();
            throw new Error(`HTTP ${res.status}: ${txt}`);
          }
          const data = await res.json();
          transcriptEl.textContent = data.transcript || "—";
          responseEl.textContent = data.response_text || "—";
          if (data.audio_url){ audioEl.src = data.audio_url; }
          setStatus("Done");
        }catch(err){
          setStatus(`Error: ${err.message || err}`);
        }finally{
          if (btnRecord) btnRecord.disabled = false;
        }
      };

      mediaRecorder.start();
    }catch(err){
      setStatus(`Mic error: ${err.message || err}`);
      if (btnRecord) btnRecord.disabled = false;
    }
  }

  function stopRecording(){
    if (mediaRecorder && mediaRecorder.state === 'recording'){
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach(t => t.stop());
    }
  }

  function playResponse(){
    if (audioEl.src){ audioEl.play().catch(()=>{}); }
  }

  if (btnRecord) btnRecord.addEventListener('click', startRecording);
  if (btnStop) btnStop.addEventListener('click', stopRecording);
  if (btnSpeak) btnSpeak.addEventListener('click', playResponse);

  // Text prompt flow
  const textInput = document.getElementById('textInput');
  const btnSend = document.getElementById('btnSend');

  async function sendText(){
    const text = (textInput?.value || "").trim();
    if (!text) return;
    setStatus("Sending…");
    if (btnSend) btnSend.disabled = true;
    try{
      const res = await fetch('/api/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      if (!res.ok){
        const t = await res.text();
        throw new Error(`HTTP ${res.status}: ${t}`);
      }
      const data = await res.json();
      transcriptEl.textContent = text || "—";
      responseEl.textContent = data.response_text || "—";
      if (data.audio_url){
        audioEl.src = data.audio_url;
        audioEl.play().catch(()=>{});
      }
      if (textInput) textInput.value = "";
      setStatus("Done");
    }catch(err){
      setStatus(`Error: ${err.message || err}`);
    }finally{
      if (btnSend) btnSend.disabled = false;
    }
  }

  if (btnSend && textInput){
    btnSend.addEventListener('click', sendText);
    textInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey){
        e.preventDefault();
        sendText();
      }
    });
  }
})();
