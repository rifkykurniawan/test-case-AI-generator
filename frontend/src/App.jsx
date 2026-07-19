import { useState } from 'react';
import { generateTestCases } from './api';
import './index.css';

function App() {
  const [requirement, setRequirement] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [testCases, setTestCases] = useState([]);

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
        </div>
      )}
    </div>
  );
}

export default App;
