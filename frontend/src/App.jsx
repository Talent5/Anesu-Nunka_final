import React, { useState, useCallback, useEffect } from 'react'
import axios from 'axios'
import Header from './components/Header'
import Footer from './components/Footer'
import PatientForm from './components/PatientForm'
import RiskResult from './components/RiskResult'
import LoadingSpinner from './components/LoadingSpinner'
import LoginPage from './components/LoginPage'
import { ClipboardList, AlertCircle } from 'lucide-react'

const API_BASE = '/api'

function App() {
  const [user, setUser] = useState(null)
  const [authChecked, setAuthChecked] = useState(false)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Check if already logged in (session cookie persists)
  useEffect(() => {
    fetch('/api/auth/status')
      .then(res => res.json())
      .then(data => {
        if (data.authenticated) setUser(data.user)
      })
      .catch(() => {})
      .finally(() => setAuthChecked(true))
  }, [])

  const handleLogin = useCallback((userData) => {
    setUser(userData)
  }, [])

  const handleLogout = useCallback(async () => {
    await fetch('/api/auth/logout', { method: 'POST' })
    setUser(null)
    setResult(null)
    setError(null)
  }, [])

  const handlePredict = useCallback(async (patientData) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_BASE}/predict`, {
        patient_data: patientData
      }, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 15000
      })

      if (response.data.success) {
        setResult(response.data)
      } else {
        setError(response.data.error || 'Prediction failed')
      }
    } catch (err) {
      if (err.response) {
        if (err.response.status === 401) {
          setUser(null)
          return
        }
        const data = err.response.data
        if (data.validation_errors) {
          setError(`Validation errors:\n${data.validation_errors.join('\n')}`)
        } else {
          setError(data.error || `Server error (${err.response.status})`)
        }
      } else if (err.code === 'ECONNABORTED') {
        setError('Request timed out. Please ensure the backend server is running.')
      } else {
        setError('Unable to connect to the prediction server. Please ensure the backend is running on port 5000.')
      }
    } finally {
      setLoading(false)
    }
  }, [])

  const handleReset = useCallback(() => {
    setResult(null)
    setError(null)
  }, [])

  // Wait for auth check before rendering
  if (!authChecked) {
    return (
      <div className="login-page">
        <div className="spinner" />
      </div>
    )
  }

  // Show login page if not authenticated
  if (!user) {
    return <LoginPage onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <Header user={user} onLogout={handleLogout} />
      
      <div className="app-container">
        {error && (
          <div className="alert alert-error" style={{ marginBottom: 24 }}>
            <AlertCircle size={18} style={{ flexShrink: 0, marginTop: 1 }} />
            <div style={{ whiteSpace: 'pre-line' }}>{error}</div>
          </div>
        )}

        <div className="main-grid">
          {/* Left Panel — Patient Data Form */}
          <div>
            <div className="card">
              <div className="card-header">
                <div className="card-header-icon" style={{ background: 'var(--primary-50)', color: 'var(--primary)' }}>
                  <ClipboardList size={20} />
                </div>
                <div>
                  <h2>Patient Assessment</h2>
                  <p style={{ fontSize: 12, color: 'var(--gray-400)', marginTop: 2 }}>
                    Enter clinical, demographic &amp; lifestyle indicators
                  </p>
                </div>
              </div>
              <div className="card-body">
                <PatientForm 
                  onSubmit={handlePredict}
                  onReset={handleReset}
                  loading={loading}
                />
              </div>
            </div>
          </div>

          {/* Right Panel — Results */}
          <div>
            {loading ? (
              <div className="card">
                <LoadingSpinner />
              </div>
            ) : result ? (
              <RiskResult data={result} />
            ) : (
              <div className="card">
                <div className="placeholder-state">
                  <div className="placeholder-icon">
                    <ClipboardList size={36} color="var(--primary-light)" />
                  </div>
                  <h3>Awaiting Patient Data</h3>
                  <p>
                    Complete the patient assessment form and click 
                    "Analyze Risk" to generate a risk stratification report.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}

export default App
