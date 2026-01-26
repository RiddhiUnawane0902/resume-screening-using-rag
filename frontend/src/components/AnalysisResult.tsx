import React from 'react';

interface AnalysisResultProps {
    data: {
        match_score: number;
        strengths: string[];
        missing_skills: string[];
        overall_assessment: string;
    } | null;
    loading: boolean;
}

const AnalysisResult: React.FC<AnalysisResultProps> = ({ data, loading }) => {
    if (loading) {
        return <div className="card"><h2>Analyzing...</h2><p>Using RAG to compare Resume against JD...</p></div>;
    }

    if (!data) return null;

    return (
        <div className="card result-card">
            <h2>Analysis Result</h2>

            <div className="score-container">
                <span className="score-label">Match Score</span>
                <span className={`score-value ${data.match_score > 70 ? 'high' : 'low'}`}>
                    {data.match_score}%
                </span>
            </div>

            <p className="summary"><strong>Summary:</strong> {data.overall_assessment}</p>

            <div className="lists-container">
                <div className="list-box strengths">
                    <h3>✅ Strengths</h3>
                    <ul>
                        {data.strengths.map((s, i) => <li key={i}>{s}</li>)}
                    </ul>
                    {data.strengths.length === 0 && <p>No specific strengths found relative to requirements.</p>}
                </div>

                <div className="list-box missing">
                    <h3>❌ Missing / Gaps</h3>
                    <ul>
                        {data.missing_skills.map((s, i) => <li key={i}>{s}</li>)}
                    </ul>
                    {data.missing_skills.length === 0 && <p>No major gaps found.</p>}
                </div>
            </div>
        </div>
    );
};

export default AnalysisResult;
