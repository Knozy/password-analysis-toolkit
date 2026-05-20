from app.core.entropy_calculator import EntropyCalculator

calculator = EntropyCalculator()

password = "MyP@ssw0rd123!"

shannon = calculator.calculate_shannon_entropy(password)
charset = calculator.calculate_entropy_by_charset(password)

rating, description = calculator.get_entropy_rating(charset)

print(f"Password: {password}")
print(f"Shannon Entropy: {shannon:.2f} bits")
print(f"Charset Entropy: {charset:.2f} bits")
print(f"Rating: {rating}")
print(f"Description: {description}")
