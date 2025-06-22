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