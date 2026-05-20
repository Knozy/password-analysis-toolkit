# app/services/report_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import io

class ReportGenerator:
    """Generate PDF and HTML reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=1  # Center
        ))
    
    def generate_pdf_report(self, analysis_results, output_path=None):
        """
        Generate PDF report from analysis results
        
        Args:
            analysis_results (dict): Results from password analyzer
            output_path (str): Where to save PDF (if None, returns bytes)
            
        Returns:
            bytes or file path
        """
        # Create PDF document
        if output_path:
            doc = SimpleDocTemplate(output_path, pagesize=letter)
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Build story
        story = []
        
        # Title
        story.append(Paragraph(
            "Password Analysis Report",
            self.styles['CustomTitle']
        ))
        
        # Date
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # Security Summary
        story.append(Paragraph("Security Summary", self.styles['Heading2']))
        
        summary_data = [
            ["Metric", "Value"],
            ["Strength Score", f"{analysis_results['strength']['score']}/100"],
            ["Strength Level", analysis_results['strength']['level']],
            ["Entropy (Charset)", f"{analysis_results['entropy']['charset_entropy']:.2f} bits"],
            ["Recommendation", analysis_results['overall_assessment']['recommendation']],
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Detailed Analysis
        story.append(Paragraph("Detailed Analysis", self.styles['Heading2']))
        
        # Characteristics
        chars = analysis_results['characteristics']
        story.append(Paragraph("<b>Password Characteristics:</b>", self.styles['Normal']))
        characteristics_text = f"""
        • Length: {chars['length']} characters<br/>
        • Lowercase: {'Yes' if chars['has_lowercase'] else 'No'}<br/>
        • Uppercase: {'Yes' if chars['has_uppercase'] else 'No'}<br/>
        • Digits: {'Yes' if chars['has_digits'] else 'No'}<br/>
        • Special Characters: {'Yes' if chars['has_special_chars'] else 'No'}<br/>
        • Character Types: {chars['character_types_count']}/4<br/>
        """
        story.append(Paragraph(characteristics_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        story.append(Paragraph("<b>Improvement Suggestions:</b>", self.styles['Normal']))
        suggestions_text = "<br/>".join([
            f"• {sugg}" for sugg in analysis_results['strength']['feedback']
        ])
        story.append(Paragraph(suggestions_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        if output_path:
            return output_path
        else:
            buffer.seek(0)
            return buffer.getvalue()
    
    def generate_html_report(self, analysis_results):
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Password Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #1f4788; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #1f4788; color: white; }}
                .score {{ font-size: 24px; font-weight: bold; }}
                .strong {{ color: green; }}
                .weak {{ color: red; }}
                .timestamp {{ color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <h1>Password Analysis Report</h1>
            <p class="timestamp">Generated: {datetime.now().isoformat()}</p>
            
            <h2>Security Summary</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Strength Score</td>
                    <td class="score {analysis_results['strength']['level'].lower().replace(' ', '_')}">{analysis_results['strength']['score']}/100</td>
                </tr>
                <tr>
                    <td>Strength Level</td>
                    <td class="{analysis_results['strength']['level'].lower().replace(' ', '_')}">{analysis_results['strength']['level']}</td>
                </tr>
                <tr>
                    <td>Entropy (Charset)</td>
                    <td>{analysis_results['entropy']['charset_entropy']:.2f} bits</td>
                </tr>
                <tr>
                    <td>Entropy Rating</td>
                    <td>{analysis_results['entropy']['rating']}</td>
                </tr>
            </table>
            
            <h2>Recommendations</h2>
            <ul>
                {''.join([f"<li>{sugg}</li>" for sugg in analysis_results['strength']['feedback']])}
            </ul>
            
            <h2>Disclaimer</h2>
            <p>
                <strong>Educational Purpose Only:</strong> This report is generated for educational 
                and authorized security testing purposes only. Unauthorized access to computer systems 
                or testing without permission is illegal.
            </p>
        </body>
        </html>
        """
        return html
