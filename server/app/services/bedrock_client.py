# app/services/bedrock_client.py
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from ..config import BEDROCK_MODEL_CLAUDE_INSTANT, BEDROCK_MODEL_TITAN_TEXT, BEDROCK_MODEL_EMBEDDING
import json

REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_IDS = {
    "claude": BEDROCK_MODEL_CLAUDE_INSTANT,
    "titan": BEDROCK_MODEL_TITAN_TEXT,
}

client = boto3.client("bedrock-runtime", region_name=REGION)

def call_bedrock_model(model_key: str, prompt: str) -> str:
    model_id = MODEL_IDS.get(model_key)
    if not model_id:
        raise ValueError(f"Unsupported model key: {model_key}")

    try:
        if "claude" in model_id:
            # Claude requires special Anthropic format
            native_request = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "temperature": 0.0, # Set to 0.0 for deterministic output 
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
            }

            # Convert the native request to JSON.
            request = json.dumps(native_request)
            json_output_key = "text"

        else:  
            # Titan
            native_request = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 1024,
                    "temperature": 0.0,
                },
            }

            # Convert the native request to JSON.
            request = json.dumps(native_request)
            json_output_key = "outputText"

        response = client.invoke_model(
            body=request,
            modelId=model_id,
            contentType="application/json",
            accept="application/json"
        )

        model_response = json.loads(response["body"].read())

        # Extract and print the response text.
        response_text = model_response["content"][0][json_output_key]
        return response_text

    except (BotoCoreError, ClientError) as e:
        print(f"ERROR: Can't invoke {model_id}.\nREASON:  {str(e)}")
        raise RuntimeError(f"ERROR: Can't invoke {model_id}.\nREASON:  {str(e)}")


def call_embedding_model(text: str) -> list:
    try:
        native_request = {
            "inputText": text
        }
        request = json.dumps(native_request)
        response = client.invoke_model(
            modelId=BEDROCK_MODEL_EMBEDDING,
            body=request,
            contentType="application/json",
            accept="application/json"
        )
        model_response = json.loads(response["body"].read())
        return model_response["embedding"]

    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to get embedding: {str(e)}")