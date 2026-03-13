import React from 'react'
import { Activity, LogOut } from 'lucide-react'

function Header({ user, onLogout }) {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="header-brand">
          <div className="header-icon">
            <Activity size={24} color="white" />
          </div>
          <div>
            <div className="header-title">Diabetes Risk Stratification</div>
            <div className="header-subtitle">Explainable AI Decision-Support System</div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div className="header-badge">
            <span className="dot"></span>
            System Active
          </div>
          {user && (
            <button
              onClick={onLogout}
              className="header-logout-btn"
              title="Sign out"
            >
              <LogOut size={16} />
              Logout
            </button>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header
