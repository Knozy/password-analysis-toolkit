# tests/test_analyzer.py
import pytest
from app.core.password_analyzer import PasswordAnalyzer
from app.core.entropy_calculator import EntropyCalculator
from app.core.strength_scorer import StrengthScorer

@pytest.fixture
def analyzer():
    return PasswordAnalyzer()

@pytest.fixture
def entropy_calc():
    return EntropyCalculator()

class TestEntropyCalculation:
    def test_shannon_entropy(self, entropy_calc):
        """Test Shannon entropy calculation"""
        # All same characters: low entropy
        entropy = entropy_calc.calculate_shannon_entropy("aaaaa")
        assert entropy < 2
        
        # Random characters: high entropy
        entropy = entropy_calc.calculate_shannon_entropy("a1B!x")
        assert entropy > 2
    
    def test_charset_entropy(self, entropy_calc):
        """Test charset-based entropy"""
        # Only lowercase: low entropy
        entropy = entropy_calc.calculate_entropy_by_charset("password")
        assert 35 < entropy < 40
        
        # Mixed case + digits + special: high entropy
        entropy = entropy_calc.calculate_entropy_by_charset("MyP@assword123!")
        assert entropy > 70

class TestStrengthScoring:
    def test_very_weak_password(self, analyzer):
        """Test scoring of very weak password"""
        result = analyzer.analyze_password("123")
        assert result['strength']['level'] == 'Very Weak'
        assert result['strength']['score'] < 20
    
    def test_weak_password(self, analyzer):
        """Test scoring of weak password"""
        result = analyzer.analyze_password("password")
        assert result['strength']['level'] in ['Very Weak', 'Weak']
        assert result['strength']['score'] < 50
    
    def test_strong_password(self, analyzer):
        """Test scoring of strong password"""
        result = analyzer.analyze_password("MyP@ssword123!")
        assert result['strength']['level'] in ['Good', 'Strong']
        assert result['strength']['score'] >= 70

class TestAttackSimulations:
    def test_brute_force_calculation(self, analyzer):
        """Test brute-force time calculation"""
        result = analyzer.analyze_password("test1234")
        
        assert 'attacks' in result
        assert 'brute_force_local' in result['attacks']
        
        brute = result['attacks']['brute_force_local']
        assert 'time_to_crack_seconds' in brute
        assert 'vulnerability_level' in brute

# Run tests
# pytest tests/test_analyzer.py -v
