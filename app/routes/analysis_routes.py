
# app/routes/analysis_routes.py
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.core.password_analyzer import PasswordAnalyzer
from app.models.user_model import AnalysisRecord, db
from datetime import datetime

bp = Blueprint('analysis', __name__, url_prefix='/api')

analyzer = PasswordAnalyzer()

@bp.route('/analyze-password', methods=['POST'])
@cross_origin()
def analyze_password():
    """
    Analyze password strength
    
    Request JSON:
    {
        "password": "password_to_analyze",
        "include_attacks": true/false
    }
    """
    try:
        data = request.get_json()

        if not data or 'password' not in data:
            return jsonify({'error': 'Password required'}), 400

        password = data.get('password', '')
        include_attacks = data.get('include_attacks', True)

        # Validate password length
        if len(password) == 0:
            return jsonify({'error': 'Password cannot be empty'}), 400
        if len(password) > 255:
            return jsonify({'error': 'Password exceeds maximum length'}), 400

        # Analyze password
        results = analyzer.analyze_password(password, include_attacks)

        # Store in database (if user is logged in)
        # user_id = current_user.id if current_user.is_authenticated else None
        # record = AnalysisRecord(
        #     user_id=user_id,
        #     password_length=len(password),
        #     entropy_value=results['entropy']['charset_entropy'],
        #     strength_score=results['strength']['score'],
        #     strength_level=results['strength']['level'],
        #     improvement_suggestions=results['strength']['feedback']
        # )
        # db.session.add(record)
        # db.session.commit()

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Analyze multiple passwords from CSV/text file
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Read file and parse passwords
        passwords = []
        if file.filename.endswith('.txt'):
            passwords = file.read().decode('utf-8').split('\n')
        elif file.filename.endswith('.csv'):
            import csv
            passwords = [row[0] for row in csv.reader(file)]

        # Analyze all passwords
        results = []
        for password in passwords:
            if password.strip():
                result = analyzer.analyze_password(password.strip(), include_attacks=False)
                results.append(result)

        return jsonify({
            'total_passwords': len(results),
            'analyzed': results
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/analysis-history', methods=['GET'])
def get_analysis_history():
    """Get user's analysis history"""
    try:
        # user_id = current_user.id if current_user.is_authenticated else None
        # records = AnalysisRecord.query.filter_by(user_id=user_id).all()

        # return jsonify([{
        #     'record_id': r.record_id,
        #     'strength_score': r.strength_score,
        #     'strength_level': r.strength_level,
        #     'analyzed_at': r.analyzed_at.isoformat()
        # } for r in records]), 200

        return jsonify({'message': 'Feature requires authentication'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
