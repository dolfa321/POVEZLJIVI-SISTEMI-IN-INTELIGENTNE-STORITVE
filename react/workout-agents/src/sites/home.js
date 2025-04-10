import { useState } from 'react';

function Home() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setUploadMessage(`✅ Server response: ${result.message}`);
    } catch (error) {
      console.error("Upload error:", error);
      setUploadMessage("❌ Error uploading file.");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Home Page</h1>
      <p>Welcome to the Workout Predictor! Click on 'Predict' to get started.</p>

      <div style={{ marginTop: "2rem" }}>
        <h2>📤 Upload your workout file</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{ marginLeft: "1rem" }}>Upload</button>

        {uploadMessage && (
          <p style={{ marginTop: "1rem", color: "green" }}>{uploadMessage}</p>
        )}
      </div>
    </div>
  );
}

export default Home;
