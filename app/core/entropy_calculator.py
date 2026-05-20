import math
from collections import Counter

class EntropyCalculator:
    """Calculate Shannon entropy for passwords"""
    
    def calculate_shannon_entropy(self, password):
        """
        Calculate Shannon entropy of a password
        
        Args:
            password (str): Password to analyze
            
        Returns:
            float: Entropy value in bits
        """
        if not password:
            return 0.0
        
        # Count character frequencies
        char_counts = Counter(password)
        password_length = len(password)
        
        # Calculate entropy
        entropy = 0.0
        for count in char_counts.values():
            probability = count / password_length
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def calculate_entropy_by_charset(self, password):
        """
        Calculate entropy based on character set size
        
        Entropy = log₂(N^L)
        where N = character set size, L = password length
        
        Args:
            password (str): Password to analyze
            
        Returns:
            float: Entropy value in bits
        """
        # Determine character set size
        charset_size = self._get_charset_size(password)
        password_length = len(password)
        
        # Calculate entropy
        entropy = password_length * math.log2(charset_size) if charset_size > 0 else 0
        
        return entropy
    
    def _get_charset_size(self, password):
        """
        Calculate total character set size based on character types present
        
        Returns:
            int: Size of character set
        """
        charset_size = 0
        
        # Check for lowercase letters (26 characters)
        if any(c.islower() for c in password):
            charset_size += 26
        
        # Check for uppercase letters (26 characters)
        if any(c.isupper() for c in password):
            charset_size += 26
        
        # Check for digits (10 characters)
        if any(c.isdigit() for c in password):
            charset_size += 10
        
        # Check for special characters (32 common special chars)
        special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"
        if any(c in special_chars for c in password):
            charset_size += 32
        
        return charset_size
    
    def get_entropy_rating(self, entropy_bits):
        """
        Convert entropy value to rating
        
        Args:
            entropy_bits (float): Entropy in bits
            
        Returns:
            tuple: (rating, description)
        """
        if entropy_bits < 20:
            return "Very Weak", "Extremely vulnerable to attacks"
        elif entropy_bits < 40:
            return "Weak", "Vulnerable to brute-force attacks"
        elif entropy_bits < 60:
            return "Moderate", "Resistant to basic attacks"
        elif entropy_bits < 80:
            return "Strong", "Resistant to most attacks"
        else:
            return "Very Strong", "Highly resistant to attacks"
