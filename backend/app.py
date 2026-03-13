"""
Diabetes Risk Stratification Decision-Support System — Backend API
=================================================================
Flask REST API serving the explainable ML model for diabetes risk prediction.

Compliant with:
  - Input validation and sanitization
  - Structured error handling
  - Clinical-grade risk stratification with adjusted thresholds
  - SHAP-based feature contribution explanations
  - CORS configuration for frontend integration

Author: Anesu Nunkha
Institution: University of Zimbabwe — Department of Analytics and Informatics
"""

import os
import sys
import logging
from datetime import datetime
from functools import wraps

import numpy as np
import pandas as pd
import joblib
import shap
from flask import Flask, request, jsonify, session
from flask_cors import CORS

from config import Config

# ─────────────────────────────────────────────────────────────
# Application Factory
# ─────────────────────────────────────────────────────────────

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": config_class.CORS_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config_class.LOG_LEVEL),
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('dss_api.log', mode='a')
        ]
    )
    logger = logging.getLogger('DSS-API')
    
    # ─────────────────────────────────────────────────────────
    # Load Model Artifacts
    # ─────────────────────────────────────────────────────────
    
    try:
        model = joblib.load(config_class.MODEL_PATH)
        scaler = joblib.load(config_class.SCALER_PATH)
        feature_names = joblib.load(config_class.FEATURES_PATH)
        
        # Initialize SHAP explainer
        shap_explainer = shap.TreeExplainer(model)
        
        logger.info("Model artifacts loaded successfully.")
        logger.info(f"   Model type: {type(model).__name__}")
        logger.info(f"   Features: {len(feature_names)}")
        model_loaded = True
    except FileNotFoundError as e:
        logger.error(f"Model artifact not found: {e}")
        logger.error("   Run the prototype notebook first to generate model artifacts.")
        model_loaded = False
        model = scaler = feature_names = shap_explainer = None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        model_loaded = False
        model = scaler = feature_names = shap_explainer = None

    # ─────────────────────────────────────────────────────────
    # Utility Functions
    # ─────────────────────────────────────────────────────────
    
    def validate_patient_data(data):
        """Validate and sanitize patient input data."""
        errors = []
        validated = {}
        
        for feature in feature_names:
            if feature not in data:
                errors.append(f"Missing required feature: '{feature}'")
                continue
            
            try:
                value = float(data[feature])
            except (ValueError, TypeError):
                errors.append(f"Invalid value for '{feature}': must be numeric")
                continue
            
            # Range validation
            feat_range = Config.FEATURE_RANGES.get(feature)
            if feat_range:
                if value < feat_range['min'] or value > feat_range['max']:
                    errors.append(
                        f"'{feature}' value {value} out of range "
                        f"[{feat_range['min']}, {feat_range['max']}]"
                    )
                    continue
                
                # Integer enforcement for binary/ordinal features
                if feat_range['type'] in ('binary', 'ordinal'):
                    if value != int(value):
                        errors.append(f"'{feature}' must be an integer (got {value})")
                        continue
                    value = int(value)
            
            validated[feature] = value
        
        return validated, errors
    
    def predict_risk_tier(probabilities):
        """
        Multi-tier risk stratification with clinically adjusted thresholds.
        
        Thresholds are intentionally set for high screening sensitivity,
        prioritizing recall (catching at-risk individuals) over precision.
        """
        if probabilities[2] >= Config.THRESHOLD_HIGH_RISK:
            return 2
        elif probabilities[1] >= Config.THRESHOLD_MODERATE_RISK:
            return 1
        else:
            return 0
    
    def get_shap_explanations(input_scaled, risk_tier, top_n=10):
        """Generate SHAP feature contributions for a single prediction."""
        try:
            shap_values = shap_explainer.shap_values(input_scaled)
            
            # Handle both old (list of 2D arrays) and new (3D array) formats
            if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
                shap_for_class = shap_values[0, :, risk_tier]
            else:
                shap_for_class = shap_values[risk_tier][0]
            
            # Sort by absolute importance
            feature_contributions = []
            sorted_indices = np.argsort(np.abs(shap_for_class))[::-1][:top_n]
            
            for idx in sorted_indices:
                feat_name = feature_names[idx]
                shap_val = float(shap_for_class[idx])
                
                # Categorize feature
                clinical = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Stroke',
                           'HeartDiseaseorAttack', 'GenHlth', 'PhysHlth', 'MentHlth', 'DiffWalk']
                demographic = ['Age', 'Sex', 'Education', 'Income']
                
                if feat_name in clinical:
                    category = 'Clinical'
                elif feat_name in demographic:
                    category = 'Demographic'
                else:
                    category = 'Lifestyle'
                
                feature_contributions.append({
                    'feature': feat_name,
                    'shap_value': round(shap_val, 6),
                    'impact': 'increases risk' if shap_val > 0 else 'decreases risk',
                    'abs_importance': round(abs(shap_val), 6),
                    'category': category
                })
            
            return feature_contributions
        except Exception as e:
            logger.warning(f"SHAP explanation failed: {e}")
            return []
    
    def require_model(f):
        """Decorator to check if model is loaded before processing."""
        @wraps(f)
        def decorated(*args, **kwargs):
            if not model_loaded:
                return jsonify({
                    'success': False,
                    'error': 'Model not loaded. Please run the prototype notebook to generate model artifacts.',
                    'code': 'MODEL_NOT_LOADED'
                }), 503
            return f(*args, **kwargs)
        return decorated
    
    # ─────────────────────────────────────────────────────────
    # Auth Helpers
    # ─────────────────────────────────────────────────────────
    
    def login_required(f):
        """Decorator to require authentication."""
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('logged_in'):
                return jsonify({
                    'success': False,
                    'error': 'Authentication required',
                    'code': 'AUTH_REQUIRED'
                }), 401
            return f(*args, **kwargs)
        return decorated
    
    # ─────────────────────────────────────────────────────────
    # Auth Routes
    # ─────────────────────────────────────────────────────────
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Admin login endpoint."""
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if (username == config_class.ADMIN_USERNAME and
                password == config_class.ADMIN_PASSWORD):
            session['logged_in'] = True
            session['username'] = username
            logger.info(f"Admin login successful: {username}")
            return jsonify({
                'success': True,
                'user': {'username': username, 'role': 'admin'}
            })
        
        logger.warning(f"Failed login attempt for username: {username}")
        return jsonify({
            'success': False,
            'error': 'Invalid username or password'
        }), 401
    
    @app.route('/api/auth/logout', methods=['POST'])
    def logout():
        """Logout endpoint."""
        session.clear()
        return jsonify({'success': True, 'message': 'Logged out'})
    
    @app.route('/api/auth/status', methods=['GET'])
    def auth_status():
        """Check current authentication status."""
        if session.get('logged_in'):
            return jsonify({
                'success': True,
                'authenticated': True,
                'user': {'username': session.get('username'), 'role': 'admin'}
            })
        return jsonify({'success': True, 'authenticated': False})
    
    # ─────────────────────────────────────────────────────────
    # API Routes
    # ─────────────────────────────────────────────────────────
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy' if model_loaded else 'degraded',
            'model_loaded': model_loaded,
            'model_type': type(model).__name__ if model else None,
            'num_features': len(feature_names) if feature_names else 0,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'version': '1.0.0',
            'thresholds': {
                'high_risk': Config.THRESHOLD_HIGH_RISK,
                'moderate_risk': Config.THRESHOLD_MODERATE_RISK
            }
        })
    
    @app.route('/api/features', methods=['GET'])
    @login_required
    @require_model
    def get_features():
        """Return feature metadata for the frontend form."""
        features_meta = []
        for feat in feature_names:
            meta = Config.FEATURE_RANGES.get(feat, {})
            
            # Human-readable labels and descriptions
            labels = {
                'HighBP': {'label': 'High Blood Pressure', 'description': 'Has the patient been told they have high blood pressure?', 'group': 'Clinical'},
                'HighChol': {'label': 'High Cholesterol', 'description': 'Has the patient been told they have high cholesterol?', 'group': 'Clinical'},
                'CholCheck': {'label': 'Cholesterol Check', 'description': 'Cholesterol check in the past 5 years?', 'group': 'Clinical'},
                'BMI': {'label': 'Body Mass Index (BMI)', 'description': 'Body Mass Index (kg/m²)', 'group': 'Clinical'},
                'Smoker': {'label': 'Smoker', 'description': 'Has the patient smoked at least 100 cigarettes in their lifetime?', 'group': 'Lifestyle'},
                'Stroke': {'label': 'History of Stroke', 'description': 'Has the patient ever had a stroke?', 'group': 'Clinical'},
                'HeartDiseaseorAttack': {'label': 'Heart Disease / Attack', 'description': 'Coronary heart disease (CHD) or myocardial infarction (MI)?', 'group': 'Clinical'},
                'PhysActivity': {'label': 'Physical Activity', 'description': 'Physical activity in the past 30 days (not including job)?', 'group': 'Lifestyle'},
                'Fruits': {'label': 'Fruit Consumption', 'description': 'Consumes fruit 1 or more times per day?', 'group': 'Lifestyle'},
                'Veggies': {'label': 'Vegetable Consumption', 'description': 'Consumes vegetables 1 or more times per day?', 'group': 'Lifestyle'},
                'HvyAlcoholConsump': {'label': 'Heavy Alcohol Consumption', 'description': 'Heavy drinker (men >14 drinks/week, women >7)?', 'group': 'Lifestyle'},
                'AnyHealthcare': {'label': 'Healthcare Coverage', 'description': 'Has any kind of health care coverage?', 'group': 'Lifestyle'},
                'NoDocbcCost': {'label': "Couldn't See Doctor (Cost)", 'description': "Couldn't see a doctor in past 12 months due to cost?", 'group': 'Lifestyle'},
                'GenHlth': {'label': 'General Health', 'description': 'Self-rated general health (1=Excellent to 5=Poor)', 'group': 'Clinical'},
                'MentHlth': {'label': 'Mental Health Days', 'description': 'Days of poor mental health in the past 30 days (0-30)', 'group': 'Clinical'},
                'PhysHlth': {'label': 'Physical Health Days', 'description': 'Days of poor physical health in the past 30 days (0-30)', 'group': 'Clinical'},
                'DiffWalk': {'label': 'Difficulty Walking', 'description': 'Serious difficulty walking or climbing stairs?', 'group': 'Clinical'},
                'Sex': {'label': 'Sex', 'description': 'Biological sex (0=Female, 1=Male)', 'group': 'Demographic'},
                'Age': {'label': 'Age Category', 'description': 'Age category (1=18-24 to 13=80+)', 'group': 'Demographic'},
                'Education': {'label': 'Education Level', 'description': 'Education level (1=Never attended to 6=College graduate)', 'group': 'Demographic'},
                'Income': {'label': 'Income Level', 'description': 'Income level (1=<$10K to 8=>=75K)', 'group': 'Demographic'},
            }
            
            feat_info = labels.get(feat, {'label': feat, 'description': '', 'group': 'Other'})
            
            features_meta.append({
                'name': feat,
                'label': feat_info['label'],
                'description': feat_info['description'],
                'group': feat_info['group'],
                'type': meta.get('type', 'continuous'),
                'min': meta.get('min', 0),
                'max': meta.get('max', 100),
            })
        
        return jsonify({
            'success': True,
            'features': features_meta,
            'total': len(features_meta)
        })
    
    @app.route('/api/predict', methods=['POST'])
    @login_required
    @require_model
    def predict():
        """
        Main prediction endpoint.
        
        Accepts patient data as JSON, returns:
        - Risk tier (Low / Moderate / High)
        - Probability scores for each tier
        - SHAP-based feature explanations
        - Clinical recommendations
        """
        request_time = datetime.utcnow()
        
        # Parse request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON',
                'code': 'INVALID_CONTENT_TYPE'
            }), 400
        
        data = request.get_json()
        
        if not data or 'patient_data' not in data:
            return jsonify({
                'success': False,
                'error': 'Request must include "patient_data" object',
                'code': 'MISSING_DATA'
            }), 400
        
        # Validate input
        validated_data, validation_errors = validate_patient_data(data['patient_data'])
        
        if validation_errors:
            return jsonify({
                'success': False,
                'error': 'Input validation failed',
                'validation_errors': validation_errors,
                'code': 'VALIDATION_ERROR'
            }), 422
        
        try:
            # Prepare input
            input_df = pd.DataFrame([validated_data])[feature_names]
            input_scaled = pd.DataFrame(
                scaler.transform(input_df),
                columns=feature_names
            )
            
            # Get probabilities
            probabilities = model.predict_proba(input_scaled)[0]
            
            # Multi-tier risk stratification
            risk_tier = predict_risk_tier(probabilities)
            
            # Get recommendation
            recommendation = Config.RECOMMENDATIONS[risk_tier]
            
            # Get SHAP explanations
            feature_explanations = get_shap_explanations(input_scaled, risk_tier)
            
            # Build response
            response = {
                'success': True,
                'prediction': {
                    'risk_tier': int(risk_tier),
                    'risk_label': recommendation['tier'],
                    'risk_description': recommendation['label'],
                    'risk_color': recommendation['color'],
                },
                'probabilities': {
                    'low_risk': round(float(probabilities[0]) * 100, 2),
                    'moderate_risk': round(float(probabilities[1]) * 100, 2),
                    'high_risk': round(float(probabilities[2]) * 100, 2),
                },
                'explanation': {
                    'method': 'SHAP (SHapley Additive exPlanations)',
                    'top_features': feature_explanations,
                    'summary': recommendation['summary']
                },
                'recommendation': {
                    'actions': recommendation['actions'],
                    'follow_up': recommendation['follow_up'],
                    'severity': recommendation['tier']
                },
                'metadata': {
                    'model_type': type(model).__name__,
                    'thresholds': {
                        'high_risk': Config.THRESHOLD_HIGH_RISK,
                        'moderate_risk': Config.THRESHOLD_MODERATE_RISK
                    },
                    'timestamp': request_time.isoformat() + 'Z',
                    'disclaimer': (
                        'This tool is a decision-support aid and does NOT replace '
                        'clinical judgment. All results should be interpreted by a '
                        'qualified healthcare professional in the context of the '
                        'full clinical picture.'
                    )
                }
            }
            
            logger.info(
                f"Prediction completed: Risk Tier={risk_tier} "
                f"(P=[{probabilities[0]:.3f}, {probabilities[1]:.3f}, {probabilities[2]:.3f}])"
            )
            
            return jsonify(response), 200
            
        except Exception as e:
            logger.error(f"Prediction error: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'Internal prediction error. Please try again.',
                'code': 'PREDICTION_ERROR'
            }), 500
    
    @app.route('/api/batch-predict', methods=['POST'])
    @login_required
    @require_model
    def batch_predict():
        """Batch prediction for multiple patients."""
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        patients = data.get('patients', [])
        
        if not patients or len(patients) > 100:
            return jsonify({
                'success': False,
                'error': 'Provide 1-100 patients in "patients" array'
            }), 400
        
        results = []
        for i, patient in enumerate(patients):
            validated, errors = validate_patient_data(patient)
            if errors:
                results.append({'index': i, 'success': False, 'errors': errors})
                continue
            
            try:
                input_df = pd.DataFrame([validated])[feature_names]
                input_scaled = pd.DataFrame(scaler.transform(input_df), columns=feature_names)
                probs = model.predict_proba(input_scaled)[0]
                tier = predict_risk_tier(probs)
                rec = Config.RECOMMENDATIONS[tier]
                
                results.append({
                    'index': i,
                    'success': True,
                    'risk_tier': int(tier),
                    'risk_label': rec['tier'],
                    'probabilities': {
                        'low_risk': round(float(probs[0]) * 100, 2),
                        'moderate_risk': round(float(probs[1]) * 100, 2),
                        'high_risk': round(float(probs[2]) * 100, 2),
                    }
                })
            except Exception as e:
                results.append({'index': i, 'success': False, 'errors': [str(e)]})
        
        return jsonify({
            'success': True,
            'total': len(patients),
            'results': results
        })
    
    # ─────────────────────────────────────────────────────────
    # Error Handlers
    # ─────────────────────────────────────────────────────────
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found',
            'code': 'NOT_FOUND'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            'success': False,
            'error': 'Method not allowed',
            'code': 'METHOD_NOT_ALLOWED'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR'
        }), 500
    
    return app


# ─────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "=" * 60)
    print("  DIABETES RISK STRATIFICATION — Decision Support System")
    print("  Backend API Server")
    print("=" * 60)
    print(f"  Endpoints:")
    print(f"    POST /api/auth/login   — Admin login")
    print(f"    POST /api/auth/logout  — Logout")
    print(f"    GET  /api/auth/status  — Auth status")
    print(f"    GET  /api/health       — Health check")
    print(f"    GET  /api/features     — Feature metadata")
    print(f"    POST /api/predict      — Single patient prediction")
    print(f"    POST /api/batch-predict — Batch predictions")
    print(f"")
    print(f"  Admin: username='admin' / password='admin123'")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)