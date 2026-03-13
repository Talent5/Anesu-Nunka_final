import React from 'react'

function ProbabilityChart({ probabilities }) {
  const bars = [
    { label: 'Low Risk', value: probabilities.low_risk, cls: 'low' },
    { label: 'Moderate Risk', value: probabilities.moderate_risk, cls: 'moderate' },
    { label: 'High Risk', value: probabilities.high_risk, cls: 'high' },
  ]

  return (
    <div className="prob-section">
      {bars.map((bar) => (
        <div key={bar.cls} className="prob-item">
          <span className="prob-label">{bar.label}</span>
          <div className="prob-bar-container">
            <div
              className={`prob-bar ${bar.cls}`}
              style={{ width: `${Math.max(bar.value, 4)}%` }}
            >
              <span className="prob-value">{bar.value.toFixed(1)}%</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ProbabilityChart
