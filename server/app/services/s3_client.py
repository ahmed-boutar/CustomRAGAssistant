import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from uuid import uuid4

from ..config import S3_BUCKET_NAME

s3_client = boto3.client("s3", region_name="us-east-1")

def upload_document_to_s3(user_id: str, file_name: str, file_bytes: bytes, content_type: str) -> str:
    key = f"uploads/{user_id}/{uuid4()}-{file_name}"
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
            Body=file_bytes,
            ContentType=content_type,
        )
        return key
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to upload file to S3: {str(e)}")

def generate_presigned_url(key: str, expiration: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": S3_BUCKET_NAME, "Key": key},
        ExpiresIn=expiration
    )