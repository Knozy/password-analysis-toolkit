import hashlib
import re
from datetime import datetime, UTC
from .entropy_calculator import EntropyCalculator
from .strength_scorer import StrengthScorer
from .brute_force_simulator import BruteForceSimulator

class PasswordAnalyzer:
    """Main password analysis engine"""
    
    def __init__(self):
        self.entropy_calc = EntropyCalculator()
        self.scorer = StrengthScorer()
        self.brute_force = BruteForceSimulator()
    
    def analyze_password(self, password, include_attacks=True):
        """
        Complete password analysis
        
        Args:
            password (str): Password to analyze
            include_attacks (bool): Include attack simulations
            
        Returns:
            dict: Complete analysis results
        """
        # Basic validation
        if not password:
            return {'error': 'Password cannot be empty'}
        
        if len(password) > 255:
            return {'error': 'Password exceeds maximum length'}
        
        # Calculate entropy
        shannon_entropy = self.entropy_calc.calculate_shannon_entropy(password)
        charset_entropy = self.entropy_calc.calculate_entropy_by_charset(password)
        entropy_rating, entropy_desc = self.entropy_calc.get_entropy_rating(charset_entropy)
        
        # Score strength
        strength_result = self.scorer.calculate_strength_score(password)
        
        # Analyze characteristics
        characteristics = self._analyze_characteristics(password)
        
        # Run attack simulations
        attacks = {}
        if include_attacks:
            attacks['brute_force_online'] = self.brute_force.simulate_brute_force(
                password, 'online'
            )
            attacks['brute_force_local'] = self.brute_force.simulate_brute_force(
                password, 'local_cpu'
            )
            attacks['brute_force_gpu'] = self.brute_force.simulate_brute_force(
                password, 'gpu'
            )
        
        # Generate hash samples
        hashes = self._generate_hash_samples(password)
        
        # Compile complete analysis
        return {
            'input': {
                'password_length': len(password),
                'timestamp': datetime.now(UTC).isoformat()
            },
            'entropy': {
                'shannon_entropy': round(shannon_entropy, 2),
                'charset_entropy': round(charset_entropy, 2),
                'rating': entropy_rating,
                'description': entropy_desc
            },
            'strength': strength_result,
            'characteristics': characteristics,
            'attacks': attacks,
            'hashes': hashes,
            'overall_assessment': self._generate_assessment(strength_result, entropy_rating)
        }
    
    def _analyze_characteristics(self, password):
        """Analyze password characteristics"""
        return {
            'length': len(password),
            'has_lowercase': any(c.islower() for c in password),
            'has_uppercase': any(c.isupper() for c in password),
            'has_digits': any(c.isdigit() for c in password),
            'has_special_chars': any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/`~" for c in password),
            'character_types_count': sum([
                any(c.islower() for c in password),
                any(c.isupper() for c in password),
                any(c.isdigit() for c in password),
                any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/`~" for c in password)
            ]),
            'contains_sequences': self._check_sequences(password),
            'contains_repeated_chars': self._check_repeated_chars(password)
        }
    
    def _check_sequences(self, password):
        """Check for sequential characters"""
        sequences = []
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and 
                ord(password[i+2]) == ord(password[i+1]) + 1):
                sequences.append(password[i:i+3])
        return sequences
    
    def _check_repeated_chars(self, password):
        """Check for repeated characters"""
        repeated = {}
        for char in set(password):
            count = password.count(char)
            if count > 2:
                repeated[char] = count
        return repeated
    
    def _generate_hash_samples(self, password):
        """Generate hash samples for demonstration"""
        return {
            'md5': hashlib.md5(password.encode()).hexdigest(),
            'sha1': hashlib.sha1(password.encode()).hexdigest(),
            'sha256': hashlib.sha256(password.encode()).hexdigest(),
            'sha512': hashlib.sha512(password.encode()).hexdigest()
        }
    
    def _generate_assessment(self, strength_result, entropy_rating):
        """Generate overall assessment"""
        score = strength_result['score']
        level = strength_result['level']
        
        if score >= 75:
            security = "Excellent"
            recommendation = "This password meets strong security standards"
        elif score >= 55:
            security = "Good"
            recommendation = "This password is reasonably secure but can be improved"
        elif score >= 35:
            security = "Fair"
            recommendation = "This password needs improvement for better security"
        else:
            security = "Poor"
            recommendation = "This password is weak and should be changed immediately"
        
        return {
            'security_level': security,
            'recommendation': recommendation,
            'score': score,
            'strength_level': level
        }
