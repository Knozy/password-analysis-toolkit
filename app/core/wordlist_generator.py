import os
import random
from collections import defaultdict

class WordlistGenerator:
    """Generate custom wordlists for dictionary attacks"""
    
    def __init__(self):
        self.patterns = {
            'dates': self._generate_dates,
            'numbers': self._generate_numbers,
            'common_words': self._generate_common_words,
            'keyboard_patterns': self._generate_keyboard_patterns,
            'custom_mutations': self._generate_mutations
        }
    
    def generate_wordlist(self, base_words, patterns=None, output_file=None):
        """
        Generate comprehensive wordlist from base words
        
        Args:
            base_words (list): Base words to expand
            patterns (list): Patterns to apply
            output_file (str): Save to file if provided
            
        Returns:
            list: Generated wordlist
        """
        wordlist = set()
        
        # Add base words
        for word in base_words:
            wordlist.add(word)
        
        # Apply patterns
        for word in base_words:
            if patterns is None or 'mutations' in patterns:
                wordlist.update(self._generate_mutations(word))
            
            if patterns is None or 'numbers' in patterns:
                wordlist.update(self._add_numbers(word))
            
            if patterns is None or 'special' in patterns:
                wordlist.update(self._add_special_chars(word))
            
            if patterns is None or 'capitalization' in patterns:
                wordlist.update(self._add_capitalization_variants(word))
        
        # Save to file if specified
        if output_file:
            self.save_wordlist(list(wordlist), output_file)
        
        return list(wordlist)
    
    def _generate_mutations(self, word):
        """Generate word mutations"""
        mutations = set()
        
        # Reverse
        mutations.add(word[::-1])
        
        # Leet speak
        leet_map = {'a': '@', 'e': '3', 'i': '!', 'o': '0', 's': '$', 't': '7'}
        leet = word
        for char, replacement in leet_map.items():
            leet = leet.replace(char, replacement)
        mutations.add(leet)
        
        # Phonetic variations
        phonetic_map = {'c': 'k', 'ph': 'f'}
        for old, new in phonetic_map.items():
            mutations.add(word.replace(old, new))
        
        return mutations
    
    def _add_numbers(self, word):
        """Add number variations"""
        variations = set()
        
        # Year variations (1900-2050)
        for year in range(1970, 2025):
            variations.add(f"{word}{year}")
            variations.add(f"{year}{word}")
        
        # Single numbers
        for i in range(10):
            variations.add(f"{word}{i}")
            variations.add(f"{word}{i}{i}")
        
        return variations
    
    def _add_special_chars(self, word):
        """Add special character variations"""
        special_chars = "!@#$%^&*()-_=+[]{}|;:',.<>?"
        variations = set()
        
        for char in special_chars:
            variations.add(f"{word}{char}")
            variations.add(f"{char}{word}")
        
        return variations
    
    def _add_capitalization_variants(self, word):
        """Add capitalization variations"""
        return {
            word.lower(),
            word.upper(),
            word.capitalize(),
            word[0].upper() + word[1:].lower()
        }
    
    def _generate_dates(self):
        """Generate date-based passwords"""
        dates = set()
        for month in range(1, 13):
            for day in range(1, 32):
                dates.add(f"{month:02d}{day:02d}")
                dates.add(f"{day:02d}{month:02d}")
        return dates
    
    def _generate_numbers(self):
        """Generate number sequences"""
        return {str(i).zfill(6) for i in range(1000000, 1001000)}
    
    def _generate_common_words(self):
        """Generate common English words"""
        return {
            'password', 'password123', 'letmein', 'welcome', 'monkey',
            'dragon', 'master', 'sunshine', 'love', 'admin'
        }
    
    def _generate_keyboard_patterns(self):
        """Generate keyboard pattern variations"""
        patterns = set()
        keyboard_rows = [
            'qwerty', 'asdfgh', 'zxcvbn',
            '123456', '789456'
        ]
        
        for row in keyboard_rows:
            patterns.add(row)
            patterns.add(row[::-1])
            for i in range(len(row)-2):
                patterns.add(row[i:i+3])
        
        return patterns
    
    def save_wordlist(self, wordlist, filepath):
        """Save wordlist to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for word in sorted(set(wordlist)):
                f.write(f"{word}\n")
        
        return len(wordlist)
    
    def load_wordlist(self, filepath):
        """Load wordlist from file"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
