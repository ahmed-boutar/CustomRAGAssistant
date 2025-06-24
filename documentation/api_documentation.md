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

### Upload `/upload`

#### `POST /upload/document`

Uploads a `.pdf` or `.docx` file, extracts text, chunks, embeds, stores in Pinecone and S3.

- **Form Fields:**
  - `file`: Binary file

---

### Inference `/inference/query`

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

