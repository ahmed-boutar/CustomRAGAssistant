# server/app/services/embedder.py
import os
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from .bedrock_client import call_embedding_model

def get_embeddings(chunks: list[str]) -> list[list[float]]:
    return [call_embedding_model(chunk) for chunk in chunks]
