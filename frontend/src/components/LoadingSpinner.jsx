import React from 'react'

function LoadingSpinner() {
  return (
    <div className="loading-overlay">
      <div className="spinner"></div>
      <div className="loading-text">Analyzing patient risk profile...</div>
      <p style={{ fontSize: 12, color: 'var(--gray-400)' }}>
        Running model inference and generating SHAP explanations
      </p>
    </div>
  )
}

export default LoadingSpinner
