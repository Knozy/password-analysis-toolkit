`javascript
// app/static/js/password_analyzer.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analyzerForm');
    const passwordInput = document.getElementById('passwordInput');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const noResultsMessage = document.getElementById('noResultsMessage');

    // Show/Hide Password
    togglePasswordBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.innerHTML = type === 'password' ? 
            '<i class="fas fa-eye"></i>' : 
            '<i class="fas fa-eye-slash"></i>';
    });

    // Analyze Password
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const password = passwordInput.value;
        const attackType = document.getElementById('attackType').value;

        if (!password) {
            alert('Please enter a password');
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

        try {
            const response = await fetch('/api/analyze-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: password,
                    include_attacks: attackType !== 'none'
                })
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data, attackType);
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error analyzing password: ' + error);
            console.error(error);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-play"></i> Analyze Password';
        }
    });

    function displayResults(data, attackType) {
        // Hide no results message
        noResultsMessage.style.display = 'none';
        resultsContainer.style.display = 'block';

        // Strength Score
        const strengthBar = document.getElementById('strengthBar');
        const scoreText = document.getElementById('scoreText');
        const strengthLevel = document.getElementById('strengthLevel');
        const score = data.strength.score;

        strengthBar.style.width = score + '%';
        strengthBar.setAttribute('aria-valuenow', score);
        scoreText.textContent = score + '/100';
        strengthLevel.textContent = data.strength.level;

        // Update color based on score
        strengthBar.className = 'progress-bar';
        if (score >= 80) strengthBar.classList.add('bg-success');
        else if (score >= 60) strengthBar.classList.add('bg-info');
        else if (score >= 40) strengthBar.classList.add('bg-warning');
        else strengthBar.classList.add('bg-danger');

        // Character Types
        const chars = data.characteristics;
        const charTypesHtml = `
            <div class="badge ${chars.has_lowercase ? 'bg-success' : 'bg-light text-dark'}">
                <i class="fas fa-check"></i> Lowercase
            </div>
            <div class="badge ${chars.has_uppercase ? 'bg-success' : 'bg-light text-dark'}">
                <i class="fas fa-check"></i> Uppercase
            </div>
            <div class="badge ${chars.has_digits ? 'bg-success' : 'bg-light text-dark'}">
                <i class="fas fa-check"></i> Digits
            </div>
            <div class="badge ${chars.has_special_chars ? 'bg-success' : 'bg-light text-dark'}">
                <i class="fas fa-check"></i> Special Chars
            </div>
        `;
        document.getElementById('characterTypes').innerHTML = charTypesHtml;

        // Score Breakdown
        const breakdown = data.strength.breakdown;
        const breakdownHtml = `
            <div class="col-md-6">
                <p><strong>Length:</strong> ${breakdown.length}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Complexity:</strong> ${breakdown.complexity}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Entropy:</strong> ${breakdown.entropy}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Pattern:</strong> ${breakdown.pattern}</p>
            </div>
        `;
        document.getElementById('scoreBreakdown').innerHTML = breakdownHtml;

        // Entropy Analysis
        document.getElementById('shannonEntropy').textContent = data.entropy.shannon_entropy.toFixed(2);
        document.getElementById('charsetEntropy').textContent = data.entropy.charset_entropy.toFixed(2);
        document.getElementById('entropyRating').textContent = data.entropy.rating;
        document.getElementById('entropyDesc').textContent = data.entropy.description;

        // Hash Samples
        document.getElementById('hashMD5').textContent = data.hashes.md5;
        document.getElementById('hashSHA256').textContent = data.hashes.sha256;

        // Suggestions
        const suggestionsList = data.strength.feedback.split(' | ');
        const suggestionsHtml = suggestionsList
            .map(s => `<li><i class="fas fa-arrow-right"></i> ${s}</li>`)
            .join('');
        document.getElementById('suggestions').innerHTML = suggestionsHtml;

        // Attack Results (if requested)
        const attackResults = document.getElementById('attackResults');
        if (data.attacks && Object.keys(data.attacks).length > 0) {
            let attackHtml = '';

            for (const [attackName, attackData] of Object.entries(data.attacks)) {
                const attackType = attackName.replace('_', ' ').toUpperCase();
                attackHtml += `
                    <div class="alert alert-warning mb-3">
                        <h6>${attackType}</h6>
                        <p>
                            <strong>Time to Crack:</strong> ${attackData.time_to_crack_human}<br>
                            <strong>Vulnerability:</strong> ${attackData.vulnerability_level}<br>
                            <strong>Charset Size:</strong> ${attackData.charset_size}<br>
                            <strong>Total Combinations:</strong> ${formatNumber(attackData.total_combinations)}
                        </p>
                    </div>
                `;
            }

            document.getElementById('attackContent').innerHTML = attackHtml;
            attackResults.style.display = 'block';
        }
    }

    // Export Functions
    document.getElementById('exportJSON').addEventListener('click', function() {
        // Implementation for JSON export
        alert('JSON export coming soon');
    });

    document.getElementById('generateReport').addEventListener('click', function() {
        // Implementation for PDF generation
        alert('PDF report generation coming soon');
    });

    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
});
