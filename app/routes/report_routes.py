# app/routes/report_routes.py

from flask import Blueprint, render_template, request, send_file, jsonify
from app.services.report_generator import ReportGenerator
from app.core.password_analyzer import PasswordAnalyzer
import io

bp = Blueprint('reports', __name__)

analyzer = PasswordAnalyzer()
report_generator = ReportGenerator()


@bp.route('/reports')
def reports_page():
    return render_template('reports.html')


@bp.route('/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()

        password = data.get('password')

        if not password:
            return jsonify({'error': 'Password required'}), 400

        # Analyze password
        results = analyzer.analyze_password(password)

        # Generate PDF
        pdf_data = report_generator.generate_pdf_report(results)

        return send_file(
            io.BytesIO(pdf_data),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='password_report.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
