# app/core/strength_scorer.py

import re
import math

class StrengthScorer:

    def calculate_strength_score(self, password):
        """
        Calculate password strength score
        Returns:
            {
                'score': int,
                'level': str,
                'feedback': list,
                'breakdown': dict
            }
        """

        score = 0
        breakdown = {}

        # -----------------------------
        # Length Score
        # -----------------------------
        length = len(password)

        if length >= 16:
            length_score = 30
        elif length >= 12:
            length_score = 25
        elif length >= 8:
            length_score = 20
        elif length >= 6:
            length_score = 10
        else:
            length_score = 0

        score += length_score
        breakdown['length'] = length_score

        # -----------------------------
        # Character Variety
        # -----------------------------
        variety_score = 0

        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if has_lower:
            variety_score += 10

        if has_upper:
            variety_score += 10

        if has_digit:
            variety_score += 10

        if has_special:
            variety_score += 15

        score += variety_score
        breakdown['character_variety'] = variety_score

        # -----------------------------
        # Complexity Bonus
        # -----------------------------
        complexity_bonus = 0

        if has_lower and has_upper:
            complexity_bonus += 5

        if has_digit and has_special:
            complexity_bonus += 5

        if length >= 12 and has_special:
            complexity_bonus += 5

        score += complexity_bonus
        breakdown['complexity_bonus'] = complexity_bonus

        # -----------------------------
        # Penalty for Common Passwords
        # -----------------------------
        common_passwords = [
            'password',
            '123456',
            '12345678',
            'qwerty',
            'admin',
            'welcome',
            'letmein',
            'abc123'
        ]

        common_penalty = 0

        if password.lower() in common_passwords:
            common_penalty = 30
            score -= common_penalty

        breakdown['common_password_penalty'] = -common_penalty

        # -----------------------------
        # Penalty for Repeated Characters
        # -----------------------------
        repeat_penalty = 0

        if re.search(r'(.)\1{2,}', password):
            repeat_penalty = 10
            score -= repeat_penalty

        breakdown['repeat_penalty'] = -repeat_penalty

        # -----------------------------
        # Clamp Score
        # -----------------------------
        score = max(0, min(score, 100))

        # -----------------------------
        # Determine Strength Level
        # -----------------------------
        level = self.determine_strength_level(score)

        # -----------------------------
        # Generate Feedback
        # -----------------------------
        feedback = self._generate_feedback(password, score)

        return {
            'score': score,
            'level': level,
            'feedback': feedback,
            'breakdown': breakdown
        }

    def determine_strength_level(self, score):
        """
        Convert numeric score into strength label
        """

        if score < 20:
            return 'Very Weak'

        elif score < 40:
            return 'Weak'

        elif score < 60:
            return 'Fair'

        elif score < 80:
            return 'Good'

        else:
            return 'Strong'

    def _generate_feedback(self, password, score):
        """
        Generate improvement suggestions
        """

        feedback = []

        if len(password) < 8:
            feedback.append("Use at least 8 characters")

        if len(password) < 12:
            feedback.append("Consider using 12+ characters for stronger security")

        if not any(c.islower() for c in password):
            feedback.append("Add lowercase letters")

        if not any(c.isupper() for c in password):
            feedback.append("Add uppercase letters")

        if not any(c.isdigit() for c in password):
            feedback.append("Add numbers")

        if not any(not c.isalnum() for c in password):
            feedback.append("Add special characters")

        common_patterns = [
            'password',
            '1234',
            'qwerty',
            'admin'
        ]

        for pattern in common_patterns:
            if pattern in password.lower():
                feedback.append("Avoid common words or patterns")
                break

        if score >= 80:
            feedback.append("Excellent password strength")

        return feedback
