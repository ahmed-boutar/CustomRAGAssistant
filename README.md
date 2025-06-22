# CustomRAGAssistant
A web app that allows user to spin up their own models through AWS Bedrock (no data retention) and upload their own documents to have a personal assistants



## Project Structure 
```
server/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entry point
│   ├── database.py      # Database connection
│   ├── models.py        # Database models (tables)
│   ├── schemas.py       # Pydantic models (API input/output)
│   ├── auth.py          # Authentication logic
│   └── config.py        # Configuration settings
├── tests/
├── requirements.txt
├── .env
├── .gitignore           
└── README.md
```


# FastAPI Authentication System - Project Report

## Executive Summary

This project implements a robust, production-ready authentication system using FastAPI and PostgreSQL. The system provides secure user registration, login, JWT-based authentication, and refresh token management with comprehensive test coverage.

## Tech Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Uvicorn**: ASGI server for running the FastAPI application

### Database & ORM
- **PostgreSQL**: Production-grade relational database
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapping (ORM)
- **Alembic**: Database migration tool (via SQLAlchemy)

### Authentication & Security
- **JWT (JSON Web Tokens)**: Stateless authentication mechanism
- **python-jose**: JWT encoding/decoding library
- **Passlib with bcrypt**: Password hashing and verification
- **Pydantic**: Data validation and serialization

### Testing Framework
- **pytest**: Advanced testing framework
- **pytest-cov**: Test coverage reporting
- **SQLite**: In-memory database for isolated testing

## System Architecture

### Core Components

#### 1. Authentication Flow
The system implements a dual-token authentication strategy:

**Registration Process:**
- User submits credentials (email, name, password)
- Password is hashed using bcrypt
- User record is created in PostgreSQL database
- Returns user profile (excluding sensitive data)

**Login Process:**
- Validates user credentials against database
- Generates two JWT tokens:
  - **Access Token**: Short-lived (30 minutes) for API access
  - **Refresh Token**: Long-lived (7 days) for token renewal
- Stores refresh token in database for server-side control

**Token Refresh Mechanism:**
- Client uses refresh token to obtain new access tokens
- Old refresh token is revoked and replaced
- Maintains security while providing seamless user experience

#### 2. Database Schema

**Users Table:**
- Primary user information (email, name, hashed password)
- Account status and timestamps
- Unique email constraint for user identification

**Refresh Tokens Table:**
- Secure token storage with expiration tracking
- User relationship via foreign key
- Revocation status for logout functionality
- Enables server-side session control

#### 3. Security Features

**Password Security:**
- Bcrypt hashing with salt rounds
- Never stores plain text passwords
- Secure password verification

**JWT Security:**
- Cryptographically signed tokens
- Configurable expiration times
- Token type differentiation (access vs refresh)

**Session Management:**
- Server-side refresh token control
- Proper logout implementation via token revocation
- Protection against token replay attacks

## API Endpoints

### Authentication Routes (`/auth`)

1. **POST /auth/register**
   - Creates new user account
   - Validates email format and required fields
   - Returns user profile information

2. **POST /auth/login**
   - Authenticates user credentials
   - Returns access and refresh tokens
   - Stores refresh token in database

3. **GET /auth/me**
   - Returns current user information
   - Requires valid access token
   - Demonstrates protected endpoint usage

4. **POST /auth/refresh**
   - Renews access token using refresh token
   - Implements token rotation for security
   - Validates token against database

5. **POST /auth/logout**
   - Revokes refresh token
   - Effectively logs user out of system
   - Prevents future token refresh

## Testing Strategy

### Test Coverage Areas

#### Unit Tests
- Password hashing and verification
- Database connection and table creation
- Individual function testing

#### Integration Tests
- Complete authentication flows
- API endpoint testing
- Database interaction validation

#### Security Tests
- Invalid token handling
- Expired token management
- Duplicate registration prevention
- Unauthorized access protection

### Test Implementation

**Test Database Isolation:**
- Uses SQLite for fast, isolated testing
- Each test runs in clean database state
- No interference between test cases

**Comprehensive Scenarios:**
- Happy path testing (successful operations)
- Error condition testing (invalid inputs)
- Edge case testing (duplicate actions, expired tokens)
- End-to-end workflow testing

**Test Statistics:**
- 25+ individual test cases
- Coverage of all authentication endpoints
- Both positive and negative test scenarios
- Integration flow testing

## Key Benefits

### Security
- Industry-standard authentication practices
- Secure password handling
- Proper session management
- Protection against common vulnerabilities

### Scalability
- Stateless JWT architecture
- Database-optimized queries
- Efficient token management
- Ready for horizontal scaling

### Maintainability
- Clean, modular code structure
- Comprehensive test coverage
- Clear separation of concerns
- Well-documented API endpoints

### Developer Experience
- Automatic API documentation (FastAPI Swagger)
- Type hints and validation
- Clear error messages
- Easy local development setup

## Future Enhancements

1. **Email Verification**: Add email confirmation for new registrations
2. **Password Reset**: Implement secure password recovery flow
3. **Rate Limiting**: Add API rate limiting for security
4. **OAuth Integration**: Support for social login providers
5. **Multi-Factor Authentication**: Add 2FA support
6. **Audit Logging**: Track authentication events

## Conclusion

This authentication system demonstrates production-ready practices for secure user management in modern web applications. The combination of FastAPI's performance, PostgreSQL's reliability, and comprehensive testing ensures a robust foundation for any application requiring user authentication.

The implementation follows security best practices while maintaining clean, testable code that can serve as a template for larger applications or microservices architectures.



## Testing 

Run pytest --cov=server.app from the root directory and it will run all tests in the server directory