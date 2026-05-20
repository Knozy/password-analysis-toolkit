# app/routes/attack_routes.py
from flask import Blueprint, request, jsonify
from app.core.brute_force_simulator import BruteForceSimulator
from app.core.dictionary_simulator import DictionaryAttackSimulator

bp = Blueprint('attacks', __name__, url_prefix='/api')

@bp.route('/simulate-brute-force', methods=['POST'])
def simulate_brute_force():
    """Simulate brute-force attack"""
    try:
        data = request.get_json()
        password = data.get('password')
        attack_type = data.get('attack_type', 'local_cpu')

        if not password:
            return jsonify({'error': 'Password required'}), 400

        simulator = BruteForceSimulator()
        results = simulator.simulate_brute_force(password, attack_type)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/simulate-dictionary', methods=['POST'])
def simulate_dictionary():
    """Simulate dictionary attack"""
    try:
        data = request.get_json()
        password = data.get('password')
        wordlist = data.get('wordlist', [])

        if not password:
            return jsonify({'error': 'Password required'}), 400

        simulator = DictionaryAttackSimulator()
        results = simulator.simulate_dictionary_attack(password, wordlist)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/generate-wordlist', methods=['POST'])
def generate_wordlist():
    """Generate custom wordlist"""
    try:
        data = request.get_json()
        base_words = data.get('base_words', [])
        patterns = data.get('patterns')

        from app.core.wordlist_generator import WordlistGenerator
        generator = WordlistGenerator()
        wordlist = generator.generate_wordlist(base_words, patterns)

        return jsonify({
            'wordlist_size': len(wordlist),
            'wordlist': wordlist[:1000]  # Return first 1000 for preview
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
