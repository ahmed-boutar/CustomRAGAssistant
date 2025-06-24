## API Documentation (FastAPI)

### Authentication Routes `/auth`

#### `POST /auth/register`

Registers a new user.

- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securePassword"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

#### `POST /auth/login`

Authenticates a user and returns JWT tokens.

- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "...",
    "refresh_token": "..."
  }
  ```

#### `GET /auth/me`

Returns current authenticated user.

- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

#### `POST /auth/refresh`

Rotates and returns a new access token.

- **Request Body:**
  ```json
  {
    "refresh_token": "..."
  }
  ```

#### `POST /auth/logout`

Revokes the current refresh token.

---

### 💬 Chat Sessions `/sessions`

#### `POST /sessions/`

Creates a new chat session.

- **Request Body:**
  ```json
  {
    "title": "My New Session"
  }
  ```
- **Response:**
  ```json
  {
    "id": 12,
    "title": "My New Session",
    "created_at": "2024-06-01T..."
  }
  ```

#### `GET /sessions/`

Returns all user sessions.

- **Response:**
  ```json
  [
    {
      "id": 12,
      "title": "My New Session",
      "created_at": "...",
      "updated_at": "..."
    }
  ]
  ```

#### `GET /sessions/{session_id}/messages`

Returns all messages in a session.

- **Response:**
  ```json
  [
    {
      "id": 3,
      "role": "user",
      "content": "What is RAG?",
      "created_at": "..."
    }
  ]
  ```

#### `DELETE /sessions/{session_id}`

Deletes a user session.

---

### 📤 Upload `/upload`

#### `POST /upload/document`

Uploads a `.pdf` or `.docx` file, extracts text, chunks, embeds, stores in Pinecone and S3.

- **Form Fields:**
  - `file`: Binary file

---

### 🧠 Inference `/inference/query`

#### `POST /inference/query`

- **Request Body:**
  ```json
  {
    "query": "What is RAG?",
    "model": "claude",
    "enable_rag": true,
    "session_id": 12
  }
  ```
- **Response:**
  ```json
  {
    "response": "Retrieval-Augmented Generation (RAG)..."
  }
  ```

---

## 🛡️ 2. Security Measures & Responsible AI

### 🔐 Security Measures

- **JWT Authentication**: Access + Refresh tokens
- **Token Revocation**: Backend database tracks valid refresh tokens
- **bcrypt**: Password hashing using strong one-way algorithm
- **Input Validation**: Via Pydantic models
- **Session Ownership Checks**: User-specific access enforced
- **HTTPS (prod)**: Assumed via cloud deployment

### 🧠 Responsible AI

- **Bedrock Use**: Claude and Titan enforce safety at the foundation layer
- **RAG Control**: Toggle gives users power over document-grounded inference
- **Prompt Filtering**: Hooks available for future moderation
- **No Training Leakage**: No user data used to fine-tune or train LLMs
- **Content Safety**: Adheres to Bedrock provider safety filters

---

## 🔏 3. Privacy Controls & Compliance

### 🔐 Privacy Controls

- **User Isolation**:
  - Documents indexed and stored with user-specific S3 folders and Pinecone namespaces
- **No Model Retention**:
  - Bedrock does not retain prompts or outputs
- **File Access**:
  - Only authenticated users can upload or query documents
- **Prompt Logging**:
  - Debug only (no long-term storage)

### 📄 Compliance Documentation

- **Storage Providers**:
  - S3 (encryption-at-rest)
  - PostgreSQL (hosted in cloud, authentication enabled)
- **LLM Providers**:
  - Amazon Bedrock (enterprise-grade compliance & auditability)
- **Data Residency**:
  - Configurable via AWS Region
- **Access Logging**:
  - Available at infrastructure level via CloudTrail (if configured)
- **PII Protections**:
  - No PII is stored in logs
  - Strong password hashing
  - Users control document lifecycle (upload/delete)

---

Each of these documents can now be placed in `documentation/`:

- `api_documentation.md`
- `security_and_responsible_ai.md`
- `privacy_and_compliance.md`

