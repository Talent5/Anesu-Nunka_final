import React from 'react'

function Footer() {
  return (
    <footer className="footer">
      <p>
        <strong>Diabetes Risk Stratification DSS</strong> — Capstone Prototype<br />
        Anesu Nunkha &middot; Supervisor: Dr. M. Muduva &middot; University of Zimbabwe, Analytics &amp; Informatics<br />
        Model: Balanced Random Forest + SHAP/LIME &middot; Dataset: CDC BRFSS 2015
      </p>
      <p style={{ marginTop: 8, fontSize: 11, color: 'var(--gray-400)' }}>
        For academic demonstration purposes only. Not for clinical use without proper validation and regulatory approval.
      </p>
    </footer>
  )
}

export default Footer
