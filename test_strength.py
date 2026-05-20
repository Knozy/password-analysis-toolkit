from app.core.strength_scorer import StrengthScorer

scorer = StrengthScorer()

password = "MyP@ssw0rd123!"

result = scorer.calculate_strength_score(password)

print(result)
