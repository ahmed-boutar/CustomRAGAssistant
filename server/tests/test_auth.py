# tests/test_auth.py
import pytest
import sys
import os
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.app.main import app
from server.app.database import Base, get_db
from server.app.models import User, RefreshToken
from server.app.auth import get_password_hash, verify_password

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    """Create tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123"
    }

@pytest.fixture
def registered_user(setup_database, sample_user_data):
    """Create a registered user for testing"""
    response = client.post("/auth/register", json=sample_user_data)
    return response.json()

class TestDatabaseConnection:
    """Test database connectivity and setup"""
    
    def test_database_connection(self, setup_database):
        """Test if we can connect to the test database"""
        connection = engine.connect()
        assert connection is not None
        connection.close()
    
    def test_tables_creation(self, setup_database):
        """Test if tables are created properly"""
        # Check if tables exist by trying to query them
        db = TestingSessionLocal()
        try:
            # This should not raise an error if tables exist
            db.query(User).first()
            db.query(RefreshToken).first()
        except Exception as e:
            pytest.fail(f"Tables not created properly: {e}")
        finally:
            db.close()

class TestPasswordHashing:
    """Test password hashing functionality"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        # Should be able to verify the password
        assert verify_password(password, hashed) is True
        # Wrong password should fail
        assert verify_password("wrongpassword", hashed) is False

class TestUserRegistration:
    """Test user registration functionality"""
    
    def test_successful_registration(self, setup_database, sample_user_data):
        """Test successful user registration"""
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["first_name"] == sample_user_data["first_name"]
        assert data["last_name"] == sample_user_data["last_name"]
        assert "id" in data
        assert "created_at" in data
        assert data["is_active"] is True
        # Password should not be in response
        assert "password" not in data
        assert "hashed_password" not in data
    
    def test_duplicate_email_registration(self, setup_database, sample_user_data):
        """Test registration with duplicate email"""
        # Register first user
        client.post("/auth/register", json=sample_user_data)
        
        # Try to register again with same email
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_invalid_email_registration(self, setup_database):
        """Test registration with invalid email"""
        invalid_data = {
            "email": "invalid-email",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword123"
        }
        
        response = client.post("/auth/register", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_missing_fields_registration(self, setup_database):
        """Test registration with missing required fields"""
        incomplete_data = {
            "email": "test@example.com",
            "first_name": "Test"
            # Missing last_name and password
        }
        
        response = client.post("/auth/register", json=incomplete_data)
        assert response.status_code == 422

class TestUserLogin:
    """Test user login functionality"""
    
    def test_successful_login(self, registered_user, sample_user_data):
        """Test successful user login"""
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        # Tokens should be non-empty strings
        assert len(data["access_token"]) > 0
        assert len(data["refresh_token"]) > 0
    
    def test_login_wrong_password(self, registered_user, sample_user_data):
        """Test login with wrong password"""
        login_data = {
            "email": sample_user_data["email"],
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, setup_database):
        """Test login with non-existent user"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "somepassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_invalid_email_format(self, setup_database):
        """Test login with invalid email format"""
        login_data = {
            "email": "invalid-email",
            "password": "somepassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 422  # Validation error

class TestAuthenticatedEndpoints:
    """Test endpoints that require authentication"""
    
    def test_get_current_user_with_valid_token(self, registered_user, sample_user_data):
        """Test getting current user info with valid token"""
        # First login to get token
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Use token to get user info
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["first_name"] == sample_user_data["first_name"]
        assert data["last_name"] == sample_user_data["last_name"]
    
    def test_get_current_user_without_token(self, setup_database):
        """Test getting current user info without token"""
        response = client.get("/auth/me")
        assert response.status_code == 403  # Forbidden
    
    def test_get_current_user_with_invalid_token(self, setup_database):
        """Test getting current user info with invalid token"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401

class TestRefreshToken:
    """Test refresh token functionality"""
    
    def test_successful_token_refresh(self, registered_user, sample_user_data):
        """Test successful token refresh"""
        # Login to get tokens
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        original_access_token = login_response.json()["access_token"]
        original_refresh_token = login_response.json()["refresh_token"]

        time.sleep(1)
        
        # Use refresh token to get new tokens
        response = client.post("/auth/refresh", params={"refresh_token": original_refresh_token})
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        
        # New tokens should be different from old ones due to different timestamps
        assert data["access_token"] != original_access_token
        assert data["refresh_token"] != original_refresh_token

        # Verify the new access token works
        headers = {"Authorization": f"Bearer {data['access_token']}"}
        me_response = client.get("/auth/me", headers=headers)
        assert me_response.status_code == 200
        
        # Verify old refresh token is now invalid (since you revoke it)
        old_refresh_response = client.post("/auth/refresh", params={"refresh_token": original_refresh_token})
        assert old_refresh_response.status_code == 401
    
    def test_refresh_with_invalid_token(self, setup_database):
        """Test refresh with invalid token"""
        response = client.post("/auth/refresh", params={"refresh_token": "invalid_token"})
        
        assert response.status_code == 401
        assert "Invalid or expired refresh token" in response.json()["detail"]
    
    def test_refresh_with_revoked_token(self, registered_user, sample_user_data):
        """Test refresh with revoked token"""
        # Login to get tokens
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout (which revokes the refresh token)
        client.post("/auth/logout", params={"refresh_token": refresh_token})
        
        # Try to use the revoked refresh token
        response = client.post("/auth/refresh", params={"refresh_token": refresh_token})
        
        assert response.status_code == 401
        assert "Invalid or expired refresh token" in response.json()["detail"]

class TestLogout:
    """Test logout functionality"""
    
    def test_successful_logout(self, registered_user, sample_user_data):
        """Test successful logout"""
        # Login to get tokens
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout
        response = client.post("/auth/logout", params={"refresh_token": refresh_token})
        
        assert response.status_code == 200
        assert "Successfully logged out" in response.json()["message"]
    
    def test_logout_with_invalid_token(self, setup_database):
        """Test logout with invalid refresh token"""
        response = client.post("/auth/logout", params={"refresh_token": "invalid_token"})
        
        assert response.status_code == 400
        assert "Invalid refresh token" in response.json()["detail"]
    
    # def test_logout_twice_with_same_token(self, registered_user, sample_user_data):
    #     """Test logging out twice with the same token"""
    #     # Login to get tokens
    #     login_data = {
    #         "email": sample_user_data["email"],
    #         "password": sample_user_data["password"]
    #     }
    #     login_response = client.post("/auth/login", json=login_data)
    #     refresh_token = login_response.json()["refresh_token"]
        
    #     # First logout
    #     response1 = client.post("/auth/logout", params={"refresh_token": refresh_token})
    #     assert response1.status_code == 200
        
    #     # Second logout with same token should fail because token is now deleted
    #     response2 = client.post("/auth/logout", params={"refresh_token": refresh_token})
    #     assert response2.status_code == 400

class TestIntegrationFlow:
    """Test complete authentication flow"""
    
    def test_complete_auth_flow(self, setup_database, sample_user_data):
        """Test complete registration -> login -> authenticated request -> refresh -> logout flow"""
        
        # 1. Register
        register_response = client.post("/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        # 2. Login
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        tokens = login_response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        
        # 3. Make authenticated request
        headers = {"Authorization": f"Bearer {access_token}"}
        me_response = client.get("/auth/me", headers=headers)
        assert me_response.status_code == 200
        
        # 4. Refresh tokens
        refresh_response = client.post("/auth/refresh", params={"refresh_token": refresh_token})
        assert refresh_response.status_code == 200
        
        new_tokens = refresh_response.json()
        new_refresh_token = new_tokens["refresh_token"]
        
        # 5. Logout
        logout_response = client.post("/auth/logout", params={"refresh_token": new_refresh_token})
        assert logout_response.status_code == 200
        
        # 6. Try to refresh with logged out token (should fail)
        final_refresh = client.post("/auth/refresh", params={"refresh_token": new_refresh_token})
        assert final_refresh.status_code == 401

if __name__ == "__main__":
    print("🧪 Running authentication tests...")
    print("Run with: pytest tests/test_auth.py -v")
    print("Or run specific test class: pytest tests/test_auth.py::TestUserLogin -v")