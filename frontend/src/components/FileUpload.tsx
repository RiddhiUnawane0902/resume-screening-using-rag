import React, { useState } from 'react';
import axios from 'axios';

interface FileUploadProps {
  onUploadSuccess: () => void;
  onAnalysisStart: (jobDescription: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess, onAnalysisStart }) => {
  const [resume, setResume] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleResumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setResume(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!resume) {
      setMessage("Please select a resume file.");
      return;
    }
    
    setLoading(true);
    setMessage("Uploading resume...");

    const formData = new FormData();
    formData.append('file', resume);

    try {
      await axios.post('http://localhost:8000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage("Resume uploaded successfully!");
      onUploadSuccess();
    } catch (err) {
      console.error(err);
      setMessage("Failed to upload resume.");
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = () => {
      if(!jobDescription.trim()) {
          setMessage("Please enter or paste a Job Description.");
          return;
      }
      onAnalysisStart(jobDescription);
  }

  return (
    <div className="card">
      <h2>1. Upload Resume & JD</h2>
      
      <div className="input-group">
        <label>Upload Resume (PDF/TXT):</label>
        <input type="file" accept=".pdf,.txt" onChange={handleResumeChange} />
        <button onClick={handleUpload} disabled={loading || !resume}>
          {loading ? "Uploading..." : "Upload Resume"}
        </button>
      </div>

      <div className="input-group">
          <label>Job Description:</label>
          <textarea 
            rows={6}
            placeholder="Paste Job Description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
          <button className="primary" onClick={handleAnalyze}>
              Analyze Candidate
          </button>
      </div>

      {message && <p className="status-message">{message}</p>}
    </div>
  );
};

export default FileUpload;
