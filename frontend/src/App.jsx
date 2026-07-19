import { useState } from 'react';
import { generateTestCases, saveTestCasesAsMarkdown } from './api';
import './index.css';

function App() {
  const [requirement, setRequirement] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [testCases, setTestCases] = useState([]);
  
  const [filename, setFilename] = useState('');
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState(null);
  const [saveError, setSaveError] = useState(null);

  const handleGenerate = async () => {
    if (!requirement.trim()) {
      setError('Please enter a software requirement first.');
      return;
    }
    
    if (requirement.trim().length < 10) {
      setError('Requirement must be at least 10 characters long.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await generateTestCases(requirement);
      setTestCases(response.testCases || []);
    } catch (err) {
      setError(err.message || 'An error occurred while generating test cases.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!filename.trim()) {
      setSaveError('Please enter a filename.');
      return;
    }

    setSaving(true);
    setSaveError(null);
    setSaveMessage(null);

    try {
      const response = await saveTestCasesAsMarkdown(filename, requirement, testCases);
      setSaveMessage(response.message || 'Successfully saved!');
    } catch (err) {
      setSaveError(err.message || 'An error occurred while saving.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>Test Case AI Generator</h1>
        <p>Transform your software requirements into structured test scenarios in seconds.</p>
      </div>

      <div className="glass-card input-section">
        <textarea
          placeholder="e.g., I have login feature, login with username and password. Create test cases"
          value={requirement}
          onChange={(e) => setRequirement(e.target.value)}
          disabled={loading}
        />
        <button onClick={handleGenerate} disabled={loading || !requirement.trim()}>
          {loading ? (
            <>
              <div className="spinner"></div>
              Generating...
            </>
          ) : (
            'Generate Test Cases'
          )}
        </button>
        {error && <div className="error-message">{error}</div>}
      </div>

      {testCases.length > 0 && (
        <div className="results-section">
          <h2>Generated Test Cases ({testCases.length})</h2>
          <div className="table-container glass-card">
            <table className="test-cases-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Test Scenario</th>
                </tr>
              </thead>
              <tbody>
                {testCases.map((tc) => (
                  <tr key={tc.id}>
                    <td className="tc-id-cell"><span className="test-case-id">{tc.id}</span></td>
                    <td>{tc.title}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="glass-card save-section" style={{ marginTop: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <h3 style={{ fontSize: '1.2rem', color: 'var(--text-color)' }}>Save as Markdown</h3>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <input
                type="text"
                placeholder="e.g., login_tests"
                value={filename}
                onChange={(e) => setFilename(e.target.value)}
                disabled={saving}
                style={{ 
                  flex: 1, 
                  background: 'var(--input-bg)', 
                  border: '1px solid var(--card-border)', 
                  borderRadius: '0.75rem', 
                  padding: '1rem', 
                  color: 'var(--text-color)',
                  fontSize: '1rem',
                  outline: 'none'
                }}
              />
              <span style={{ color: 'var(--text-color)' }}>.md</span>
              <button onClick={handleSave} disabled={saving || !filename.trim()}>
                {saving ? 'Saving...' : 'Save File'}
              </button>
            </div>
            {saveError && <div className="error-message">{saveError}</div>}
            {saveMessage && <div style={{ color: 'var(--success-color)', padding: '0.5rem 0' }}>{saveMessage}</div>}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
