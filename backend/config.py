"""
Configuration for Diabetes Risk Stratification DSS
Compliant with health data handling best practices
"""

import os

class Config:
    """Application configuration."""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'None')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # Model paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    MODEL_PATH = os.path.join(MODEL_DIR, 'diabetes_model.joblib')
    SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.joblib')
    FEATURES_PATH = os.path.join(MODEL_DIR, 'feature_names.joblib')
    
    # Risk thresholds (clinically adjusted for screening sensitivity)
    THRESHOLD_HIGH_RISK = 0.40
    THRESHOLD_MODERATE_RISK = 0.25
    
    # Admin credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    # API rate limiting
    RATE_LIMIT = os.environ.get('RATE_LIMIT', '100/hour')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Feature metadata for validation
    FEATURE_RANGES = {
        'HighBP':               {'min': 0, 'max': 1, 'type': 'binary'},
        'HighChol':             {'min': 0, 'max': 1, 'type': 'binary'},
        'CholCheck':            {'min': 0, 'max': 1, 'type': 'binary'},
        'BMI':                  {'min': 10, 'max': 80, 'type': 'continuous'},
        'Smoker':               {'min': 0, 'max': 1, 'type': 'binary'},
        'Stroke':               {'min': 0, 'max': 1, 'type': 'binary'},
        'HeartDiseaseorAttack': {'min': 0, 'max': 1, 'type': 'binary'},
        'PhysActivity':         {'min': 0, 'max': 1, 'type': 'binary'},
        'Fruits':               {'min': 0, 'max': 1, 'type': 'binary'},
        'Veggies':              {'min': 0, 'max': 1, 'type': 'binary'},
        'HvyAlcoholConsump':    {'min': 0, 'max': 1, 'type': 'binary'},
        'AnyHealthcare':        {'min': 0, 'max': 1, 'type': 'binary'},
        'NoDocbcCost':          {'min': 0, 'max': 1, 'type': 'binary'},
        'GenHlth':              {'min': 1, 'max': 5, 'type': 'ordinal'},
        'MentHlth':             {'min': 0, 'max': 30, 'type': 'continuous'},
        'PhysHlth':             {'min': 0, 'max': 30, 'type': 'continuous'},
        'DiffWalk':             {'min': 0, 'max': 1, 'type': 'binary'},
        'Sex':                  {'min': 0, 'max': 1, 'type': 'binary'},
        'Age':                  {'min': 1, 'max': 13, 'type': 'ordinal'},
        'Education':            {'min': 1, 'max': 6, 'type': 'ordinal'},
        'Income':               {'min': 1, 'max': 8, 'type': 'ordinal'},
    }
    
    # Clinical recommendations per risk tier
    RECOMMENDATIONS = {
        0: {
            'tier': 'LOW RISK',
            'label': 'Low Risk — No Diabetes Indicators',
            'color': '#10b981',
            'icon': 'shield-check',
            'summary': 'Based on the provided clinical, demographic, and lifestyle indicators, this patient shows low risk for diabetes.',
            'actions': [
                'Continue routine health monitoring',
                'Maintain current healthy lifestyle practices',
                'Schedule standard diabetes screening per ADA guidelines (every 3 years for adults ≥45)',
                'Encourage continued physical activity and balanced nutrition',
                'No immediate clinical intervention required'
            ],
            'follow_up': '3 years (routine screening)'
        },
        1: {
            'tier': 'MODERATE RISK',
            'label': 'Moderate Risk — Prediabetes Indicators',
            'color': '#f59e0b',
            'icon': 'exclamation-triangle',
            'summary': 'This patient shows moderate risk indicators consistent with prediabetes. Early intervention can prevent progression to Type 2 Diabetes.',
            'actions': [
                'Recommend confirmatory diagnostic testing (HbA1c, Fasting Plasma Glucose)',
                'Initiate lifestyle modification counseling (diet, exercise)',
                'Refer to Diabetes Prevention Program (DPP) if available',
                'Target 5-7% body weight reduction if BMI > 25',
                'Recommend 150 min/week moderate-intensity physical activity',
                'Schedule follow-up screening in 6 months',
                'Monitor blood pressure and cholesterol levels'
            ],
            'follow_up': '6 months (enhanced monitoring)'
        },
        2: {
            'tier': 'HIGH RISK',
            'label': 'High Risk — Diabetes Indicators Present',
            'color': '#ef4444',
            'icon': 'exclamation-circle',
            'summary': 'This patient presents multiple high-risk indicators for diabetes. Urgent clinical evaluation is recommended.',
            'actions': [
                'URGENT: Refer for diagnostic confirmation (HbA1c ≥ 6.5%, FPG ≥ 126 mg/dL, or OGTT ≥ 200 mg/dL)',
                'Comprehensive metabolic panel recommended',
                'Assess for diabetic complications (retinopathy, nephropathy, neuropathy)',
                'Initiate intensive lifestyle intervention immediately',
                'Consider pharmacological intervention (per clinical judgment)',
                'Cardiovascular risk assessment (given comorbidity profile)',
                'Schedule follow-up within 2-4 weeks',
                'Diabetes self-management education referral'
            ],
            'follow_up': '2-4 weeks (urgent follow-up)'
        }
    }
