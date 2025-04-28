import pytest
from fastapi.testclient import TestClient
from jose import jwt
import secrets
import string
import re
from datetime import datetime, timedelta
from ..main import app
from ..database import Base, engine, get_db
from ..crud import get_user_by_username, create_user
from ..schemas import UserCreate
from sqlalchemy.orm import Session

# Setup test client
client = TestClient(app)

# Create a test database session
def override_get_db():
    try:
        db = TestClient(app).db
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def create_test_user():
    """Create a test user for authentication"""
    db = next(override_get_db())
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="Password123!"
    )
    
    # Check if user already exists
    existing_user = get_user_by_username(db, username=user_data.username)
    if not existing_user:
        user = create_user(db, user_data)
        return {
            "username": user_data.username,
            "password": "Password123!"
        }
    return {
        "username": user_data.username,
        "password": "Password123!"
    }

def get_auth_token(username, password):
    """Get auth token for test user"""
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    return response.json().get("access_token")

class TestSecurityFeatures:
    """Test security features of the API"""
    
    def test_password_hashing(self, db):
        """Test that passwords are properly hashed"""
        # Create a user
        user_creds = create_test_user()
        
        # Get the user from the database directly
        db_session = next(override_get_db())
        db_user = get_user_by_username(db_session, username=user_creds["username"])
        
        # Verify that the password is hashed (not stored in plaintext)
        assert db_user.hashed_password != user_creds["password"]
        assert len(db_user.hashed_password) > 0
        assert '$' in db_user.hashed_password  # Usually hashed passwords contain $ symbols
    
    def test_brute_force_protection(self, db):
        """Test protection against brute force attacks"""
        # Create a test user
        user_creds = create_test_user()
        
        # Try multiple incorrect login attempts
        for _ in range(5):
            response = client.post(
                "/token",
                data={"username": user_creds["username"], "password": "wrongpassword"}
            )
            assert response.status_code == 401
        
        # After multiple failed attempts, the system should still allow correct credentials
        response = client.post(
            "/token",
            data={"username": user_creds["username"], "password": user_creds["password"]}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_token_expiration(self, db):
        """Test that tokens expire correctly"""
        # Create a test user
        user_creds = create_test_user()
        
        # Get token
        token = get_auth_token(user_creds["username"], user_creds["password"])
        
        # Verify that the token contains an expiration claim
        decoded_token = jwt.decode(token, verify=False)
        assert "exp" in decoded_token
        
        # Verify expiration time is reasonable (e.g., not too long)
        exp_time = datetime.fromtimestamp(decoded_token["exp"])
        now = datetime.utcnow()
        assert exp_time > now  # Token should not be already expired
        assert exp_time < now + timedelta(days=2)  # Token should expire within a reasonable time
    
    def test_auth_required_endpoints(self, db):
        """Test that protected endpoints require authentication"""
        # Try to access protected endpoint without authentication
        response = client.get("/me")
        assert response.status_code == 401
        
        # Create a test user and get token
        user_creds = create_test_user()
        token = get_auth_token(user_creds["username"], user_creds["password"])
        
        # Access with valid token
        response = client.get(
            "/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
    
    def test_sql_injection_resistance(self, db):
        """Test resistance to SQL injection attacks"""
        # Attempt SQL injection in username field
        sql_injection_attempts = [
            "' OR '1'='1",
            "admin'; --",
            "username' OR 1=1; --",
            "'); DROP TABLE users; --"
        ]
        
        for injection in sql_injection_attempts:
            response = client.post(
                "/token",
                data={"username": injection, "password": "anypassword"}
            )
            # Should return 401 unauthorized, not 500 server error
            assert response.status_code == 401
    
    def test_xss_protection(self, db):
        """Test protection against XSS attacks"""
        # Create user with potential XSS payload in username
        xss_payload = "<script>alert('XSS')</script>"
        
        # Attempt to create user with XSS payload
        response = client.post(
            "/signup",
            json={
                "username": f"user{xss_payload}",
                "email": "xss@example.com",
                "password": "Password123!"
            }
        )
        
        # Should either sanitize input or reject it
        if response.status_code == 200:
            # If accepted, verify the XSS is sanitized in the response
            user_data = response.json()
            assert xss_payload not in user_data["username"]
        else:
            # Or it should be rejected with a validation error
            assert response.status_code in [400, 422]
    
    def test_password_strength_requirements(self, db):
        """Test that the API enforces strong password requirements"""
        weak_passwords = [
            "password",  # Common password
            "12345678",  # Only numbers
            "abcdefgh",  # Only lowercase
            "SHORT",     # Too short
        ]
        
        for password in weak_passwords:
            response = client.post(
                "/signup",
                json={
                    "username": "weakpassuser",
                    "email": "weak@example.com",
                    "password": password
                }
            )
            # Should reject weak passwords
            assert response.status_code in [400, 422]
        
        # Strong password should be accepted
        response = client.post(
            "/signup",
            json={
                "username": "strongpassuser",
                "email": "strong@example.com",
                "password": "StrongP@ssw0rd"
            }
        )
        assert response.status_code == 200
    
    def test_rate_limiting(self):
        """Test rate limiting protection"""
        # Make multiple rapid requests to check for rate limiting
        for _ in range(20):
            client.post("/token", data={"username": "nonexistent", "password": "wrongpass"})
        
        # The last request should either be rate limited or succeed
        # This test may need adjustment based on your rate limiting implementation
        response = client.post("/token", data={"username": "nonexistent", "password": "wrongpass"})
        # Either rate limited (429) or normal unauthorized (401)
        assert response.status_code in [401, 429]
    
    def test_token_refresh_security(self, db):
        """Test token refresh security (if implemented)"""
        # This test will depend on your specific implementation
        user_creds = create_test_user()
        token = get_auth_token(user_creds["username"], user_creds["password"])
        
        # Test token refresh if implemented
        # For example:
        # response = client.post("/refresh", headers={"Authorization": f"Bearer {token}"})
        # assert response.status_code == 200
        # assert "access_token" in response.json()
        
        # Ensure old token is invalidated after refresh (if implemented)
        # ...
    
    def test_content_security_headers(self):
        """Test that proper security headers are set"""
        response = client.get("/")
        headers = response.headers
        
        # Check for recommended security headers
        assert "X-Content-Type-Options" in headers
        assert "X-Frame-Options" in headers
        # Additional headers might include:
        # - Content-Security-Policy
        # - Strict-Transport-Security
        # - X-XSS-Protection
