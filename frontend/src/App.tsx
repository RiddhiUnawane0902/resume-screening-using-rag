import { useState } from 'react'
import FileUpload from './components/FileUpload'
import AnalysisResult from './components/AnalysisResult'
import ChatInterface from './components/ChatInterface'
import axios from 'axios'
import './index.css'

function App() {
  const [analysisData, setAnalysisData] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [uploaded, setUploaded] = useState(false)

  const handleAnalysisStart = async (jobDescription: string) => {
    setAnalyzing(true);
    try {
      const res = await axios.post('http://localhost:8000/api/analyze', { job_description: jobDescription });
      setAnalysisData(res.data);
    } catch (err) {
      console.error(err);
      alert("Analysis failed. Check backend console.");
    } finally {
      setAnalyzing(false);
    }
  }

  return (
    <div className="container">
      <header>
        <h1>AI Resume Screening</h1>
        <p>RAG-Powered Analysis & Chat</p>
      </header>

      <main>
        <FileUpload
          onUploadSuccess={() => setUploaded(true)}
          onAnalysisStart={handleAnalysisStart}
        />

        {uploaded && (
          <div className="grid">
            <AnalysisResult data={analysisData} loading={analyzing} />
            <ChatInterface />
          </div>
        )}
      </main>
    </div>
  )
}

export default App
