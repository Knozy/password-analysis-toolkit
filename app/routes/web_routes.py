from flask import Blueprint, render_template, request, jsonify, make_response, send_file
from app.data.store import analysis_history
from app.core.password_analyzer import PasswordAnalyzer
from app.services.report_generator import ReportGenerator
import io

bp = Blueprint('web', __name__)

# Create analyzer object
analyzer_engine = PasswordAnalyzer()


# Home Page
@bp.route('/')
def home():
    return render_template('index.html')


# Analyzer Page
@bp.route('/analyzer')
def analyzer_page():
    return render_template('analyzer.html')


# Reports Page
@bp.route('/reports')
def reports_page():
    return render_template('reports.html')

# Attack simpulator Page
@bp.route('/attacks')
def attacks():
    return render_template('attacks.html')

# Dashboard Page
@bp.route('/dashboard')
def dashboard():

    total = len(analysis_history)

    strong = 0
    weak = 0

    for item in analysis_history:

        level = item['result']['strength']['level']

        if level in ['Strong', 'Very Strong']:
            strong += 1
        else:
            weak += 1

    return render_template(
        'dashboard.html',
        total=total,
        strong=strong,
        weak=weak,
        history=analysis_history
    )

# History Page
@bp.route('/history')
def history():

    return render_template(
        'history.html',
        history=analysis_history
    )

# Documentation Page
@bp.route('/documentation')
def documentation():

    return render_template(
        'documentation.html',
        history=analysis_history
    )

# API Route
@bp.route('/api/analyze-password', methods=['POST'])
def analyze_password_api():

    data = request.get_json()

    password = data.get('password', '')

    if not password:
        return jsonify({
            'error': 'Password required'
        }), 400

    result = analyzer_engine.analyze_password(password)
    saved_data = {
        'password': password,
        'result': result
    }

    analysis_history.append(saved_data)

    return jsonify(result)


# Generate Report
@bp.route('/generate-report', methods=['POST'])
def generate_report():

    try:

        data = request.get_json()

        password = data.get('password', '')

        if not password:
            return jsonify({
                'error': 'Password required'
            }), 400

        # Analyze password
        analysis_results = analyzer_engine.analyze_password(
            password
        )

        # Create PDF
        report_generator = ReportGenerator()

        pdf_data = report_generator.generate_pdf_report(
            analysis_results
        )

        # Send PDF properly
        response = make_response(pdf_data)

        response.headers['Content-Type'] = 'application/pdf'

        response.headers['Content-Disposition'] = (
            'attachment; filename=password_report.pdf'
        )

        return response

    except Exception as e:

        print("REPORT ERROR:", str(e))

        return jsonify({
            'error': str(e)
        }), 500
