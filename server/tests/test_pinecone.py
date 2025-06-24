# tests/test_pinecone_client.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_imports():
    print("🔍 Testing Pinecone client imports...")
    try:
        from server.app.services import pinecone_client
        print("✅ Pinecone client imported successfully!")
    except Exception as e:
        print(f"❌ Import failed: {e}")

def test_upsert_mock():
    print("🔍 Testing mock upsert to Pinecone...")
    try:
        from server.app.services import pinecone_client
        from unittest.mock import patch

        chunks = ["Chunk 1", "Chunk 2"]
        embeddings = [[0.1] * 1536, [0.2] * 1536]
        metadata = {"document_name": "MockDoc.pdf"}
        user_id = "testuser"

        with patch.object(pinecone_client.index, "upsert") as mock_upsert:
            namespace = pinecone_client.upsert_documents(user_id, chunks, embeddings, metadata)
            mock_upsert.assert_called_once()
            assert namespace == "user-testuser"
            print("✅ upsert_documents() ran successfully!")
    except Exception as e:
        print(f"❌ upsert_documents() test failed: {e}")

def test_query_mock():
    print("🔍 Testing query_similar_chunks() with mock Pinecone data...")
    try:
        from server.app.services import pinecone_client
        from unittest.mock import patch

        mock_result = {
            "matches": [
                {"score": 0.9, "metadata": {"text": "Relevant"}},
                {"score": 0.85, "metadata": {"text": "Also relevant"}}
            ]
        }

        with patch.object(pinecone_client.index, "query", return_value=mock_result):
            matches = pinecone_client.query_similar_chunks("testuser", [0.1] * 1536)
            assert len(matches) == 2
            print("✅ query_similar_chunks() returned results correctly!")
    except Exception as e:
        print(f"❌ query_similar_chunks() test failed: {e}")
        return False

def main():
    print("🧪 Running Pinecone client tests...\n")

    if not test_imports():
        print("❌ Fix import issues before continuing.")
        return

    if not test_upsert_mock():
        print("❌ Fix upsert mock logic.")
        return

    if not test_query_mock():
        print("❌ Fix query logic.")
        return

    print("\n✅ All Pinecone tests passed! 🎉")

if __name__ == "__main__":
    main()
