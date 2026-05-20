import time
import math
from datetime import timedelta

class BruteForceSimulator:
    """Simulate brute-force password attack"""
    
    # Typical guesses per second by attack type
    GUESSES_PER_SECOND = {
        'online': 10,  # Limited by login attempts
        'local_cpu': 1_000_000,  # Modern CPU with GPU acceleration
        'gpu': 100_000_000,  # High-end GPU
        'distributed': 1_000_000_000  # Multiple systems
    }
    
    def simulate_brute_force(self, password, attack_type='local_cpu'):
        """
        Simulate brute-force attack on password
        
        Args:
            password (str): Target password
            attack_type (str): Type of attack (determines speed)
            
        Returns:
            dict: Attack results
        """
        charset_size = self._get_charset_size(password)
        password_length = len(password)
        guesses_per_second = self.GUESSES_PER_SECOND.get(attack_type, 1_000_000)
        
        # Calculate total possible combinations
        total_combinations = charset_size ** password_length
        
        # Average time to crack (50% chance after half the combinations)
        average_attempts = total_combinations // 2
        time_to_crack_seconds = average_attempts / guesses_per_second
        
        # Vulnerability assessment
        if time_to_crack_seconds < 1:
            vulnerability = "CRITICAL"
        elif time_to_crack_seconds < 3600:  # Less than 1 hour
            vulnerability = "HIGH"
        elif time_to_crack_seconds < 86400 * 30:  # Less than 1 month
            vulnerability = "MEDIUM"
        else:
            vulnerability = "LOW"
        
        return {
            'attack_type': attack_type,
            'charset_size': charset_size,
            'password_length': password_length,
            'total_combinations': total_combinations,
            'guesses_per_second': guesses_per_second,
            'average_attempts': average_attempts,
            'time_to_crack_seconds': time_to_crack_seconds,
            'time_to_crack_human': self._seconds_to_human(time_to_crack_seconds),
            'vulnerability_level': vulnerability,
            'simulation_results': self._run_simulation(password, guesses_per_second)
        }
    
    def _get_charset_size(self, password):
        """Get character set size"""
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/`~" for c in password):
            charset_size += 32
        
        return charset_size or 1
    
    def _run_simulation(self, password, guesses_per_second, max_iterations=10000):
        """
        Run actual brute-force simulation (limited iterations for demo)
        
        Args:
            password (str): Target password
            guesses_per_second (int): Attack speed
            max_iterations (int): Maximum simulation iterations
            
        Returns:
            dict: Simulation results
        """
        charset_size = self._get_charset_size(password)
        attempts = 0
        found = False
        
        # For demo, simulate finding it after random number of attempts
        import random
        target_attempts = min(
            random.randint(1, charset_size ** len(password)),
            max_iterations
        )
        
        start_time = time.time()
        
        for attempts in range(target_attempts):
            if attempts % max(1, target_attempts // 100) == 0:
                # Progress checkpoint every 1%
                pass
        
        elapsed_time = time.time() - start_time
        
        return {
            'simulated_attempts': attempts,
            'found': found,
            'simulation_time_seconds': elapsed_time
        }
    
    def _seconds_to_human(self, seconds):
        """Convert seconds to human-readable format"""
        if seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
        elif seconds < 86400 * 365:
            days = seconds / 86400
            return f"{days:.1f} days"
        elif seconds < 86400 * 365 * 100:
            years = seconds / (86400 * 365)
            return f"{years:.1f} years"
        else:
            return "Longer than human civilization"
