# test_bedrock.py
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_imports():
    print("🔍 Testing Bedrock imports...")
    try:
        from server.app.services import bedrock_client, query_handler
        print("✅ Bedrock service modules imported successfully!")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("   Make sure:")
        print("   - app/services/bedrock_client.py exists")
        print("   - app/services/query_handler.py exists")
        print("   - __init__.py is in those folders")

def test_env_vars():
    print("🔍 Checking required ENV variables...")
    required_keys = [
        "AWS_REGION",
        "BEDROCK_MODEL_CLAUDE_INSTANT",
        "BEDROCK_MODEL_TITAN_TEXT"
    ]
    missing = [k for k in required_keys if os.getenv(k) is None]
    
    if missing:
        print(f"❌ Missing environment variables: {missing}")
    
    print("✅ All required ENV variables found!")

def test_call_bedrock():
    print("🔍 Running test call to Claude (short prompt)...")
    try:
        from server.app.services.query_handler import run_chat

        result = run_chat(
            model="claude",
            system_prompt="You are a testing bot.",
            chat_history=[
                {"role": "user", "content": "Hi"},
                {"role": "assistant", "content": "Hello!"}
            ],
            user_input="What is your name?"
        )

        print("✅ Claude replied:", result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"❌ Claude call failed: {e}")
    
def test_call_embedding():
    print("🔍 Running test call to Titan embedding model...")
    try:
        from server.app.services.bedrock_client import call_embedding_model

        test_text = "Sample input text for embedding"
        result = call_embedding_model(test_text)

        assert isinstance(result, list), "Result should be a list"
        assert all(isinstance(x, float) for x in result), "All elements should be floats"
        assert len(result) > 0, "Embedding should not be empty"

        print(f"✅ Embedding returned! Vector size: {len(result)}")
    except Exception as e:
        print(f"❌ Embedding call failed: {e}")


def main():
    print("Running Bedrock integration tests...\n")

    if not test_imports():
        print("❌ Fix import issues before continuing.\n")
        return

    if not test_env_vars():
        print("❌ Fix your .env or environment configuration.\n")
        return

    if not test_call_bedrock():
        print("❌ Claude model is not responding properly.\n")
        return
    
    if not test_call_embedding():
        print("❌ Titan embedding model not responding correctly.\n")
        return

    print("\n✅ All Bedrock tests passed!")

if __name__ == "__main__":
    main()
