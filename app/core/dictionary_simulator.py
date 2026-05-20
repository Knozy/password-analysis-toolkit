import hashlib
import time

class DictionaryAttackSimulator:
    """Simulate dictionary-based password attack"""
    
    def __init__(self, wordlist_path=None):
        """
        Initialize simulator with wordlist
        
        Args:
            wordlist_path (str): Path to wordlist file
        """
        self.wordlist = []
        if wordlist_path:
            self.load_wordlist(wordlist_path)
    
    def load_wordlist(self, wordlist_path):
        """Load wordlist from file"""
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.wordlist = [line.strip() for line in f if line.strip()]
            return len(self.wordlist)
        except FileNotFoundError:
            raise FileNotFoundError(f"Wordlist file not found: {wordlist_path}")
    
    def simulate_dictionary_attack(self, password, wordlist=None, max_attempts=None):
        """
        Simulate dictionary attack against password
        
        Args:
            password (str): Target password
            wordlist (list): List of candidate passwords
            max_attempts (int): Maximum attempts to simulate
            
        Returns:
            dict: Attack results
        """
        if wordlist:
            self.wordlist = wordlist
        
        if not self.wordlist:
            raise ValueError("No wordlist loaded")
        
        max_attempts = max_attempts or len(self.wordlist)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        start_time = time.time()
        attempts = 0
        found = False
        matching_word = None
        
        for word in self.wordlist[:max_attempts]:
            attempts += 1
            word_hash = hashlib.sha256(word.encode()).hexdigest()
            
            if word_hash == password_hash:
                found = True
                matching_word = word
                break
            
            # Also try with common variations
            for variation in self._generate_variations(word):
                variation_hash = hashlib.sha256(variation.encode()).hexdigest()
                if variation_hash == password_hash:
                    found = True
                    matching_word = variation
                    break
            
            if found:
                break
        
        elapsed_time = time.time() - start_time
        
        # Success rate: if password was in wordlist
        success_rate = 100.0 if found else (attempts / max_attempts) * 100
        
        return {
            'attack_type': 'dictionary',
            'wordlist_size': len(self.wordlist),
            'attempts_made': attempts,
            'found': found,
            'matching_word': matching_word,
            'time_taken_seconds': elapsed_time,
            'success_rate': success_rate,
            'vulnerability_assessment': self._assess_vulnerability(found, attempts),
            'defense_recommendations': self._generate_recommendations(password)
        }
    
    def _generate_variations(self, word):
        """Generate common password variations"""
        variations = []
        
        # Capitalization
        variations.append(word.capitalize())
        variations.append(word.upper())
        
        # Common number appends
        for i in range(10):
            variations.append(f"{word}{i}")
            variations.append(f"{word}{i}{i}")
        
        # Common special character appends
        for char in "!@#$%":
            variations.append(f"{word}{char}")
        
        return variations
    
    def _assess_vulnerability(self, found, attempts):
        """Assess vulnerability based on attack success"""
        if found:
            if attempts < 100:
                return "CRITICAL: Password found in top common passwords"
            elif attempts < 10000:
                return "HIGH: Password found in common wordlist"
            else:
                return "MEDIUM: Password found after many attempts"
        else:
            return "LOW: Password not found in dictionary (good sign)"
    
    def _generate_recommendations(self, password):
        """Generate defense recommendations"""
        recommendations = []
        
        if password.lower() in ['password', '123456', 'qwerty']:
            recommendations.append("Never use extremely common passwords")
        
        if len(password) < 12:
            recommendations.append("Increase password length to at least 12 characters")
        
        if not any(c.isdigit() for c in password):
            recommendations.append("Include numbers in password")
        
        if not any(c in "!@#$%^&*" for c in password):
            recommendations.append("Include special characters")
        
        if not recommendations:
            recommendations.append("Password appears resistant to dictionary attacks")
        
        return recommendations
    
    def create_variations_wordlist(self, base_word):
        """
        Create variations of a base word
        
        Args:
            base_word (str): Base word to create variations from
            
        Returns:
            list: List of variations
        """
        variations = set([base_word])
        
        # Add capitalization variants
        variations.add(base_word.capitalize())
        variations.add(base_word.upper())
        variations.add(base_word.lower())
        
        # Add number appends
        for i in range(100):
            variations.add(f"{base_word}{i}")
        
        # Add special character appends
        for char in "!@#$%^&*()-_=+[]{}|;:',.<>?":
            variations.add(f"{base_word}{char}")
        
        # Add reverse
        variations.add(base_word[::-1])
        
        return list(variations)
