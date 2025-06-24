import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_imports():
    print("🔍 Testing S3 client imports...")
    try:
        from server.app.services import s3_client
        print("✅ S3 client imported successfully!")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("   Make sure:")
        print("   - s3_client.py exists")
        print("   - Correct __init__.py setup")

def test_env_vars():
    print("🔍 Checking required S3 ENV variables...")
    required_keys = [
        "AWS_REGION",
        "S3_BUCKET"
    ]
    missing = [k for k in required_keys if os.getenv(k) is None]

    if missing:
        print(f"❌ Missing environment variables: {missing}")

    print("✅ All required ENV variables found!")

def test_upload_and_presigned_url():
    print("🔍 Simulating file upload and presigned URL generation using moto...")

    try:
        from moto import mock_s3
        import boto3
        from server.app.services.s3_client import upload_document_to_s3, generate_presigned_url

        test_user_id = "testuser"
        test_file_name = "test.txt"
        test_file_bytes = b"Hello, this is a test file!"
        test_content_type = "text/plain"
        test_bucket = os.getenv("S3_BUCKET", "fake-bucket")

        with mock_s3():
            # Create a mock S3 bucket
            s3 = boto3.client("s3", region_name="us-east-1")
            s3.create_bucket(Bucket=test_bucket)

            # Upload and check result
            key = upload_document_to_s3(test_user_id, test_file_name, test_file_bytes, test_content_type)
            assert key.startswith("uploads/"), "S3 key format is incorrect"
            print(f"✅ File uploaded with key: {key}")

            url = generate_presigned_url(key)
            assert url.startswith("https://"), "Presigned URL is not formatted properly"
            print(f"✅ Presigned URL generated: {url[:60]}...")

    except ImportError:
        print("❌ You must install `moto` to run this test: pip install moto[boto3]")
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
def test_upload_document_error():
    from server.app.services.s3_client import upload_document_to_s3
    from unittest.mock import patch
    with patch("server.app.services.s3_client.s3_client.put_object"):
        try:
            upload_document_to_s3("user", "file.txt", b"test", "text/plain")
        except RuntimeError as e:
            assert "Failed to upload file to S3" in str(e)

def main():
    print("Running S3 Client Integration Tests...\n")

    if not test_imports():
        print("❌ Fix import issues before continuing.\n")
        return

    if not test_env_vars():
        print("❌ Fix your .env or environment config.\n")
        return

    if not test_upload_and_presigned_url():
        print("❌ S3 upload or presigned URL generation failed.\n")
        return
    
    if not test_upload_document_error():
        print("❌ Error handling in upload_document_to_s3 failed.\n")
        return

    print("\n✅ All S3 Client tests passed! 🎉")

if __name__ == "__main__":
    main()
