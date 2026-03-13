import React, { useState, useCallback } from 'react'
import { Send, RotateCcw, Info } from 'lucide-react'

// Feature configuration with labels, types, and options
const FEATURE_CONFIG = [
  {
    group: 'Clinical Indicators',
    icon: '🏥',
    fields: [
      { name: 'HighBP', label: 'High Blood Pressure', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: 'Diagnosed with high BP' },
      { name: 'HighChol', label: 'High Cholesterol', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: 'Diagnosed with high cholesterol' },
      { name: 'CholCheck', label: 'Cholesterol Check (5yr)', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: 'Cholesterol checked in past 5 years' },
      { name: 'BMI', label: 'BMI (kg/m²)', type: 'number', min: 10, max: 80, step: 0.1, hint: 'Body Mass Index' },
      { name: 'Stroke', label: 'History of Stroke', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}] },
      { name: 'HeartDiseaseorAttack', label: 'Heart Disease / MI', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: 'CHD or heart attack' },
      { name: 'GenHlth', label: 'General Health', type: 'select', options: [{v: 1, l:'1 — Excellent'}, {v: 2, l:'2 — Very Good'}, {v: 3, l:'3 — Good'}, {v: 4, l:'4 — Fair'}, {v: 5, l:'5 — Poor'}], hint: 'Self-rated general health' },
      { name: 'MentHlth', label: 'Poor Mental Health Days', type: 'number', min: 0, max: 30, step: 1, hint: 'Days in past 30' },
      { name: 'PhysHlth', label: 'Poor Physical Health Days', type: 'number', min: 0, max: 30, step: 1, hint: 'Days in past 30' },
      { name: 'DiffWalk', label: 'Difficulty Walking', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: 'Serious difficulty walking/climbing stairs' },
    ]
  },
  {
    group: 'Demographic Information',
    icon: '👤',
    fields: [
      { name: 'Sex', label: 'Biological Sex', type: 'select', options: [{v: 0, l:'Female'}, {v: 1, l:'Male'}] },
      { 
        name: 'Age', label: 'Age Category', type: 'select',
        options: [
          {v:1,l:'1 — 18-24'},{v:2,l:'2 — 25-29'},{v:3,l:'3 — 30-34'},
          {v:4,l:'4 — 35-39'},{v:5,l:'5 — 40-44'},{v:6,l:'6 — 45-49'},
          {v:7,l:'7 — 50-54'},{v:8,l:'8 — 55-59'},{v:9,l:'9 — 60-64'},
          {v:10,l:'10 — 65-69'},{v:11,l:'11 — 70-74'},{v:12,l:'12 — 75-79'},{v:13,l:'13 — 80+'}
        ]
      },
      {
        name: 'Education', label: 'Education Level', type: 'select',
        options: [
          {v:1,l:'1 — Never attended / Kindergarten'},{v:2,l:'2 — Elementary'},
          {v:3,l:'3 — Some high school'},{v:4,l:'4 — High school graduate'},
          {v:5,l:'5 — Some college / technical'},{v:6,l:'6 — College graduate'}
        ]
      },
      {
        name: 'Income', label: 'Annual Income', type: 'select',
        options: [
          {v:1,l:'1 — <$10,000'},{v:2,l:'2 — $10-15K'},{v:3,l:'3 — $15-20K'},
          {v:4,l:'4 — $20-25K'},{v:5,l:'5 — $25-35K'},{v:6,l:'6 — $35-50K'},
          {v:7,l:'7 — $50-75K'},{v:8,l:'8 — ≥$75,000'}
        ]
      }
    ]
  },
  {
    group: 'Lifestyle Factors',
    icon: '🏃',
    fields: [
      { name: 'Smoker', label: 'Smoker (100+ cigarettes lifetime)', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}] },
      { name: 'PhysActivity', label: 'Physical Activity (30 days)', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: 'Outside of work' },
      { name: 'Fruits', label: 'Daily Fruit Consumption', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: '≥1 fruit per day' },
      { name: 'Veggies', label: 'Daily Vegetable Consumption', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: '≥1 vegetable per day' },
      { name: 'HvyAlcoholConsump', label: 'Heavy Alcohol Use', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: 'Men >14/wk, Women >7/wk' },
      { name: 'AnyHealthcare', label: 'Has Healthcare Coverage', type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}] },
      { name: 'NoDocbcCost', label: "Couldn't Afford Doctor", type: 'select', options: [{v: 0, l:'No'}, {v: 1, l:'Yes'}], hint: 'Past 12 months' },
    ]
  }
]

// Default values for quick demo
const DEFAULT_VALUES = {
  HighBP: '', HighChol: '', CholCheck: '1', BMI: '',
  Smoker: '', Stroke: '0', HeartDiseaseorAttack: '0',
  PhysActivity: '', Fruits: '', Veggies: '',
  HvyAlcoholConsump: '0', AnyHealthcare: '1', NoDocbcCost: '0',
  GenHlth: '', MentHlth: '', PhysHlth: '',
  DiffWalk: '0', Sex: '', Age: '', Education: '', Income: ''
}

// Pre-filled scenarios for demonstration
const DEMO_SCENARIOS = {
  healthy: {
    label: 'Healthy Adult',
    data: {
      HighBP: '0', HighChol: '0', CholCheck: '1', BMI: '24',
      Smoker: '0', Stroke: '0', HeartDiseaseorAttack: '0',
      PhysActivity: '1', Fruits: '1', Veggies: '1',
      HvyAlcoholConsump: '0', AnyHealthcare: '1', NoDocbcCost: '0',
      GenHlth: '1', MentHlth: '0', PhysHlth: '0',
      DiffWalk: '0', Sex: '0', Age: '3', Education: '6', Income: '7'
    }
  },
  atRisk: {
    label: 'At-Risk Patient',
    data: {
      HighBP: '1', HighChol: '1', CholCheck: '1', BMI: '32',
      Smoker: '1', Stroke: '0', HeartDiseaseorAttack: '0',
      PhysActivity: '0', Fruits: '0', Veggies: '0',
      HvyAlcoholConsump: '0', AnyHealthcare: '1', NoDocbcCost: '0',
      GenHlth: '4', MentHlth: '10', PhysHlth: '15',
      DiffWalk: '0', Sex: '1', Age: '8', Education: '4', Income: '4'
    }
  },
  highRisk: {
    label: 'High-Risk Patient',
    data: {
      HighBP: '1', HighChol: '1', CholCheck: '1', BMI: '38',
      Smoker: '1', Stroke: '1', HeartDiseaseorAttack: '1',
      PhysActivity: '0', Fruits: '0', Veggies: '0',
      HvyAlcoholConsump: '0', AnyHealthcare: '1', NoDocbcCost: '1',
      GenHlth: '5', MentHlth: '20', PhysHlth: '25',
      DiffWalk: '1', Sex: '1', Age: '11', Education: '3', Income: '2'
    }
  }
}

function PatientForm({ onSubmit, onReset, loading }) {
  const [formData, setFormData] = useState({ ...DEFAULT_VALUES })
  const [errors, setErrors] = useState({})

  const handleChange = useCallback((e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    // Clear error for this field
    setErrors(prev => {
      const next = { ...prev }
      delete next[name]
      return next
    })
  }, [])

  const validate = useCallback(() => {
    const newErrors = {}
    const allFields = FEATURE_CONFIG.flatMap(g => g.fields)
    
    allFields.forEach(field => {
      const val = formData[field.name]
      if (val === '' || val === undefined || val === null) {
        newErrors[field.name] = 'Required'
      }
    })

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }, [formData])

  const handleSubmit = useCallback((e) => {
    e.preventDefault()
    if (!validate()) return

    // Convert to numbers
    const numericData = {}
    Object.entries(formData).forEach(([key, val]) => {
      numericData[key] = parseFloat(val)
    })
    onSubmit(numericData)
  }, [formData, validate, onSubmit])

  const handleReset = useCallback(() => {
    setFormData({ ...DEFAULT_VALUES })
    setErrors({})
    onReset()
  }, [onReset])

  const loadScenario = useCallback((key) => {
    setFormData({ ...DEMO_SCENARIOS[key].data })
    setErrors({})
  }, [])

  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* Quick Demo Scenarios */}
      <div style={{ marginBottom: 20 }}>
        <div style={{ fontSize: 12, color: 'var(--gray-400)', marginBottom: 8, fontWeight: 500 }}>
          Quick demo scenarios:
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          {Object.entries(DEMO_SCENARIOS).map(([key, scenario]) => (
            <button
              key={key}
              type="button"
              className="btn btn-secondary"
              style={{ padding: '6px 14px', fontSize: 12 }}
              onClick={() => loadScenario(key)}
            >
              {scenario.label}
            </button>
          ))}
        </div>
      </div>

      {/* Feature Groups */}
      {FEATURE_CONFIG.map((group) => (
        <div key={group.group} className="form-section">
          <div className="form-section-title">
            <span>{group.icon}</span> {group.group}
          </div>
          <div className="form-grid">
            {group.fields.map((field) => (
              <div key={field.name} className="form-group">
                <label className="form-label" htmlFor={field.name}>
                  {field.label}
                  {field.hint && (
                    <span className="tooltip-wrapper">
                      <Info size={13} className="info-icon" />
                      <span className="tooltip-content">{field.hint}</span>
                    </span>
                  )}
                </label>
                
                {field.type === 'select' ? (
                  <select
                    id={field.name}
                    name={field.name}
                    className={`form-select ${errors[field.name] ? 'error' : ''}`}
                    value={formData[field.name]}
                    onChange={handleChange}
                  >
                    <option value="">Select...</option>
                    {field.options.map(opt => (
                      <option key={opt.v} value={opt.v}>{opt.l}</option>
                    ))}
                  </select>
                ) : (
                  <input
                    id={field.name}
                    name={field.name}
                    type="number"
                    className={`form-input ${errors[field.name] ? 'error' : ''}`}
                    value={formData[field.name]}
                    onChange={handleChange}
                    min={field.min}
                    max={field.max}
                    step={field.step}
                    placeholder={field.hint || `${field.min} — ${field.max}`}
                  />
                )}
                
                {errors[field.name] && (
                  <span style={{ fontSize: 11, color: 'var(--danger)' }}>{errors[field.name]}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* Action Buttons */}
      <div className="btn-group">
        <button
          type="submit"
          className="btn btn-primary btn-block"
          disabled={loading}
        >
          <Send size={16} />
          {loading ? 'Analyzing...' : 'Analyze Risk'}
        </button>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={handleReset}
          disabled={loading}
        >
          <RotateCcw size={16} />
          Reset
        </button>
      </div>
    </form>
  )
}

export default PatientForm
