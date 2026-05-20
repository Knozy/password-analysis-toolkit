import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestAnalysisAPI:
    def test_analyze_password_endpoint(self, client):
        """Test password analysis API endpoint"""
        response = client.post('/api/analyze-password', 
            json={'password': 'TestPass123!'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'strength' in data
        assert 'entropy' in data
    
    def test_missing_password(self, client):
        """Test error handling for missing password"""
        response = client.post('/api/analyze-password',
            json={}
        )
        assert response.status_code == 400
    
    def test_empty_password(self, client):
        """Test error handling for empty password"""
        response = client.post('/api/analyze-password',
            json={'password': ''}
        )
        assert response.status_code == 400
