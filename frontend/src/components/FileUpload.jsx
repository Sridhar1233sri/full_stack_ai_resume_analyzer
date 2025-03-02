import { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [analysis, setAnalysis] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage(response.data.message);
      setAnalysis(response.data.analysis);
    } catch (error) {
      console.error("Upload Error:", error);
      setMessage("Error uploading file. Check the console.");
    }
  };

  return (
    <div>
      <h2>Upload Your Resume</h2>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {message && <p>{message}</p>}
      {analysis && (
        <div>
          <h3>AI Feedback:</h3>
          <p>{analysis}</p>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
