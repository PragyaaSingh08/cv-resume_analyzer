import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const Main = () => {
  const [showUpload, setShowUpload] = useState(false);
  const [resumeFileName, setResumeFileName] = useState('');
  const [queryFileName, setQueryFileName] = useState('');
  const [resumeUploaded, setResumeUploaded] = useState(false);
  const [queryUploaded, setQueryUploaded] = useState(false);

  const resumeInputRef = useRef();
  const queryInputRef = useRef();
  const navigate = useNavigate();

  const handleEvaluateClick = () => {
    setShowUpload(true);
  };

  const handleClose = () => {
    setShowUpload(false);
    setResumeFileName('');
    setQueryFileName('');
    setResumeUploaded(false);
    setQueryUploaded(false);
  };

  return (
    <main style={{
      padding: '40px',
      textAlign: 'center',
      backgroundColor: '#f5f5f5',
      minHeight: '500px'
    }}>
      <p>Click the button below to evaluate a candidate's resume.</p>

      <button onClick={handleEvaluateClick} style={buttonStyle}>
        Evaluate
      </button>

      {showUpload && (
        <div style={overlayStyle}>
          <div style={modalStyle}>
            <button onClick={handleClose} style={closeButtonStyle}>✕</button>
            <p>Please upload a PDF resume and a CSV query file.</p>

            {/* Resume upload */}
            <div style={{ marginBottom: '20px' }}>
              <label style={{ fontWeight: 'bold' }}>Resume:</label>
              <div style={uploadFieldStyle} onClick={() => resumeInputRef.current.click()}>
                {resumeFileName || 'Click to select a PDF resume'}
              </div>
              <input
                type="file"
                accept=".pdf"
                ref={resumeInputRef}
                onChange={(e) => {
                  setResumeFileName(e.target.files[0]?.name || '');
                  setResumeUploaded(false);
                }}
                style={{ display: 'none' }}
              />
              <button
                style={{ ...buttonStyle, marginTop: '5px' }}
                onClick={async () => {
                  const file = resumeInputRef.current.files[0];
                  if (!file) return alert("Please select a PDF resume first");

                  const formData = new FormData();
                  formData.append("file", file);

                  try {
                    const res = await fetch('http://localhost:8000/upload', {
                      method: 'POST',
                      body: formData
                    });
                    if (res.ok) {
                      alert("Resume uploaded successfully!");
                      setResumeUploaded(true);
                    } else {
                      throw new Error();
                    }
                  } catch {
                    alert("Resume upload failed.");
                    setResumeUploaded(false);
                  }
                }}
              >
                Upload Resume
              </button>
            </div>

            {/* Query file upload */}
            <div style={{ marginBottom: '20px' }}>
              <label style={{ fontWeight: 'bold' }}>Query File:</label>
              <div style={uploadFieldStyle} onClick={() => queryInputRef.current.click()}>
                {queryFileName || 'Click to select a CSV query file'}
              </div>
              <input
                type="file"
                accept=".csv"
                ref={queryInputRef}
                onChange={(e) => {
                  setQueryFileName(e.target.files[0]?.name || '');
                  setQueryUploaded(false);
                }}
                style={{ display: 'none' }}
              />
              <button
                style={{ ...buttonStyle, marginTop: '10px' }}
                onClick={async () => {
                  const file = queryInputRef.current.files[0];
                  if (!file) return alert("Please select a CSV query file first");

                  const formData = new FormData();
                  formData.append("file", file);

                  try {
                    const res = await fetch('http://localhost:8000/getquery', {
                      method: 'POST',
                      body: formData
                    });
                    if (res.ok) {
                      alert("Query file uploaded successfully!");
                      setQueryUploaded(true);
                    } else {
                      throw new Error();
                    }
                  } catch {
                    alert("Query file upload failed.");
                    setQueryUploaded(false);
                  }
                }}
              >
                Upload CSV
              </button>
            </div>

            {/* Analyze and Navigate */}
            <div>
              <button
                onClick={async () => {
                  if (resumeUploaded && queryUploaded) {
                    try {
                      const safeQueryFile = queryFileName?.toLowerCase().trim() || '';

                      const res = await fetch('http://localhost:8000/resume_analyze', {
                        method: 'POST',
                        headers: {
                          'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ query_file: safeQueryFile })
                      });

                      if (!res.ok) throw new Error("Analysis failed");

                      const data = await res.json();

                      navigate('/result', {
                        state: {
                          resumeName: resumeFileName,
                          queryFileName: queryFileName,
                          averageScore: data.average || 0,
                          results: data.results || []
                        }
                      });

                      handleClose();
                    } catch (error) {
                      console.error("Analysis error:", error);
                      alert("Resume analysis failed. Please try again.");
                    }
                  } else {
                    alert('Please upload both resume and query files before proceeding.');
                  }
                }}
                style={{ ...buttonStyle, marginTop: '20px' }}
              >
                Check Result
              </button>
            </div>
          </div>
        </div>
      )}

      <section style={{ marginTop: '20px' }}>
        <div style={headingRowStyle}>
          <h3 style={{ margin: 0 }}>Evaluated Resume Descriptions</h3>
          <input type="text" placeholder="Search" style={searchInputStyle} />
        </div>

        <table style={tableStyle}>
          <thead>
            <tr style={{ backgroundColor: '#008080', color: 'white' }}>
              <th>Resume Name</th>
              <th>Query File</th>
              <th>Average Score</th>
            </tr>
          </thead>
          <tbody>
            {/* Will be rendered in Result.js */}
          </tbody>
        </table>
      </section>
    </main>
  );
};

// Styles
const buttonStyle = {
  padding: '5px 10px',
  backgroundColor: '#008080',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  fontSize: '16px',
  cursor: 'pointer'
};

const overlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100vw',
  height: '100vh',
  backgroundColor: 'rgba(0, 0, 0, 0.5)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  zIndex: 1000
};

const modalStyle = {
  backgroundColor: '#fff',
  padding: '30px',
  borderRadius: '8px',
  boxShadow: '0 0 15px rgba(0,0,0,0.3)',
  width: '90%',
  maxWidth: '500px',
  position: 'relative'
};

const closeButtonStyle = {
  position: 'absolute',
  top: '10px',
  right: '15px',
  background: 'transparent',
  border: 'none',
  fontSize: '20px',
  cursor: 'pointer',
  color: '#888'
};

const uploadFieldStyle = {
  border: '1px solid #ccc',
  padding: '10px',
  borderRadius: '5px',
  backgroundColor: '#f9f9f9',
  cursor: 'pointer',
  marginTop: '8px'
};

const tableStyle = {
  width: '100%',
  borderCollapse: 'collapse',
  marginTop: '20px'
};

const headingRowStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '10px'
};

const searchInputStyle = {
  padding: '6px',
  width: '200px',
  borderRadius: '4px',
  border: '1px solid #ccc'
};

export default Main;
