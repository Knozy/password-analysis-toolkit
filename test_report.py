from app.services.report_generator import ReportGenerator

sample = {
    "strength": {
        "score": 82,
        "level": "Strong",
        "feedback": [
            "Good password length",
            "Contains uppercase letters",
            "Contains special characters"
        ]
    },
    "entropy": {
        "charset_entropy": 78.5,
        "rating": "High"
    },
    "characteristics": {
        "length": 14,
        "has_lowercase": True,
        "has_uppercase": True,
        "has_digits": True,
        "has_special_chars": True,
        "character_types_count": 4
    },
    "overall_assessment": {
        "recommendation": "Password is secure"
    }
}

generator = ReportGenerator()

generator.generate_pdf_report(sample, "report.pdf")

print("PDF report generated successfully!")
