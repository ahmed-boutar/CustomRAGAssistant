# Security Measures, Responsible AI, and Privacy

### Security Measures

- **JWT Authentication**: Access + Refresh tokens. Access tokens are currently set to 30 minutes in which case a new token will be needed or the token will refresh automatically if the user is till using the app.
- **Token Revocation**: Backend database tracks valid refresh tokens
- **bcrypt**: Password hashing using strong one-way algorithm
- **Input Validation**: Via Pydantic models
- **Session Ownership Checks**: User-specific access enforced

### Responsible AI

- **Bedrock Use**: Claude and Titan enforce safety at the foundation layer. This guarantees that data is not persistant meaning that all user chats and LLM responses will not be sent back to the model providers.
- **RAG Control**: Toggle gives users power over document-grounded inference
- **Prompt Filtering**: Hooks available for future moderation
- **Bedrock Guardrails**: Protects from prompt injection and PII 
- All of the document chunks are stored under different namespaces in pinecone, ensuring that the model does not retrieve information pertaining to other users. The calls to pinecone are made to specific namespaces and not just the pinecone index

### Privacy Controls

- **User Isolation**:
  - Documents indexed and stored with user-specific S3 folders and Pinecone namespaces
- **No Model Retention**:
  - Bedrock does not retain prompts or outputs
- **File Access**:
  - Only authenticated users can upload or query documents. Documents are stored in secure S3 bucket under the specific username. If this app will be made available to users, we will only retain documents for up to 1 year from upload. Documents will not be used to fine-tune the model
- **Prompt Logging**:
  - Prompts are logged to provide history context to the LLM and to display it in the UI

### Compliance Documentation

- **Storage Providers**:
  - S3 (encryption-at-rest)
  - PostgreSQL (hosted in cloud, authentication enabled)
- **LLM Providers**:
  - Amazon Bedrock (enterprise-grade compliance & auditability)
- **PII Protections**:
  - No PII is stored in logs
  - Strong password hashing
  - Users control document lifecycle (upload/delete)