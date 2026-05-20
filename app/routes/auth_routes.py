from flask import Blueprint, jsonify

bp = Blueprint('auth', __name__)

@bp.route('/api/auth/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Password Analysis Toolkit API running'
    })
