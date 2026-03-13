import React from 'react'
import ProbabilityChart from './ProbabilityChart'
import FeatureExplanation from './FeatureExplanation'
import { 
  ShieldCheck, AlertTriangle, AlertOctagon, 
  BarChart3, Brain, Stethoscope, Calendar, 
  Info, CheckCircle2
} from 'lucide-react'

const RISK_ICONS = {
  0: ShieldCheck,
  1: AlertTriangle,
  2: AlertOctagon
}

const RISK_CLASSES = {
  0: 'low',
  1: 'moderate',
  2: 'high'
}

function RiskResult({ data }) {
  const { prediction, probabilities, explanation, recommendation, metadata } = data
  const riskTier = prediction.risk_tier
  const RiskIcon = RISK_ICONS[riskTier]
  const riskClass = RISK_CLASSES[riskTier]

  return (
    <div className="result-container">
      {/* Risk Banner */}
      <div className={`risk-banner ${riskClass} fade-in-up`}>
        <div className="risk-banner-icon">
          <RiskIcon size={32} color="white" />
        </div>
        <h3>{prediction.risk_label}</h3>
        <p>{prediction.risk_description}</p>
      </div>

      {/* Probability Distribution */}
      <div className="card fade-in-up delay-1">
        <div className="card-header">
          <div className="card-header-icon" style={{ background: '#f0fdf4', color: 'var(--success)' }}>
            <BarChart3 size={20} />
          </div>
          <h2>Risk Probability Distribution</h2>
        </div>
        <div className="card-body">
          <ProbabilityChart probabilities={probabilities} />
        </div>
      </div>

      {/* Feature Explanations (SHAP) */}
      <div className="card fade-in-up delay-2">
        <div className="card-header">
          <div className="card-header-icon" style={{ background: '#eff6ff', color: 'var(--primary)' }}>
            <Brain size={20} />
          </div>
          <div>
            <h2>Key Contributing Factors</h2>
            <p style={{ fontSize: 11, color: 'var(--gray-400)', marginTop: 2 }}>
              SHAP-based feature importance — explaining why this prediction was made
            </p>
          </div>
        </div>
        <div className="card-body">
          {explanation.summary && (
            <div className="alert alert-info" style={{ marginBottom: 16 }}>
              <Info size={16} style={{ flexShrink: 0, marginTop: 2 }} />
              <span>{explanation.summary}</span>
            </div>
          )}
          <FeatureExplanation features={explanation.top_features} />
        </div>
      </div>

      {/* Clinical Recommendations */}
      <div className="card fade-in-up delay-3">
        <div className="card-header">
          <div className="card-header-icon" style={{ 
            background: riskTier === 2 ? '#fee2e2' : riskTier === 1 ? '#fef3c7' : '#d1fae5',
            color: prediction.risk_color 
          }}>
            <Stethoscope size={20} />
          </div>
          <h2>Clinical Recommendations</h2>
        </div>
        <div className="card-body">
          <ul className="recommendation-list">
            {recommendation.actions.map((action, idx) => (
              <li key={idx} className="recommendation-item">
                <CheckCircle2 
                  size={18} 
                  className="recommendation-bullet"
                  color={prediction.risk_color}
                />
                <span>{action}</span>
              </li>
            ))}
          </ul>

          <div className="follow-up-badge">
            <Calendar size={16} />
            <strong>Recommended follow-up:</strong> {recommendation.follow_up}
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="disclaimer fade-in-up delay-4">
        <Info size={16} className="disclaimer-icon" />
        <div>
          <strong>Clinical Disclaimer:</strong> {metadata.disclaimer}
          <br />
          <span style={{ fontSize: 11, color: 'var(--gray-400)' }}>
            Model: {metadata.model_type} &middot; Thresholds: High &ge;{metadata.thresholds.high_risk}, 
            Moderate &ge;{metadata.thresholds.moderate_risk} &middot; 
            Timestamp: {new Date(metadata.timestamp).toLocaleString()}
          </span>
        </div>
      </div>
    </div>
  )
}

export default RiskResult
