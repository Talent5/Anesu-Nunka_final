import React from 'react'
import { TrendingUp, TrendingDown } from 'lucide-react'

function FeatureExplanation({ features }) {
  if (!features || features.length === 0) return null

  const maxAbs = Math.max(...features.map(f => f.abs_importance))

  return (
    <div>
      {features.slice(0, 8).map((feat, idx) => {
        const isPositive = feat.shap_value > 0
        const barWidth = maxAbs > 0 ? (feat.abs_importance / maxAbs) * 100 : 0
        
        return (
          <div key={feat.feature} className="explanation-item">
            <div className="explanation-rank">{idx + 1}</div>
            
            <div className="explanation-info">
              <div className="explanation-name">{feat.feature}</div>
              <div className="explanation-category">{feat.category}</div>
            </div>
            
            <div className="explanation-bar-container">
              <div className="explanation-bar-wrapper">
                <div
                  className={`explanation-bar ${isPositive ? 'positive' : 'negative'}`}
                  style={{ width: `${barWidth}%` }}
                />
              </div>
            </div>
            
            <div className={`explanation-impact ${isPositive ? 'positive' : 'negative'}`}>
              {isPositive ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <TrendingUp size={12} /> Risk
                </span>
              ) : (
                <span style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <TrendingDown size={12} /> Risk
                </span>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default FeatureExplanation
