import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload/", formData);
      setTranscript(res.data.transcript);
      setSummary(res.data.summary);
    } catch (err) {
      alert("Upload failed!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" accept="audio/*" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Upload & Summarize"}
      </button>

      {transcript && (
        <>
          <h2>Transcript</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{transcript}</pre>
        </>
      )}
      {summary && (
        <>
          <h2>Summary & Action Items</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{summary}</pre>
        </>
      )}
    </div>
  );
}

export default UploadForm;