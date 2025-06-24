# test/test_document_processor.py
import sys
import os
from pathlib import Path
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.app.database import create_tables, SessionLocal
from server.app.services.document_processor import extract_text, process_and_store_document

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    create_tables()

def test_pdf():
    BASE_DIR = Path(__file__).resolve().parents[1] 
    file_path = BASE_DIR / "samples" / "customer_interviews.pdf"
    file_bytes = file_path.read_bytes()
    filename = "customer_interviews.pdf"
    text = extract_text(file_bytes, filename)
    print("PDF Text Sample:\n", text[:500])

def test_docx():
    BASE_DIR = Path(__file__).resolve().parents[1] 
    file_path = BASE_DIR / "samples" / "ahmed_boutar-resume-ml.docx"
    filename = "ahmed_boutar-resume-ml.docx"
    file_bytes = file_path.read_bytes()
    text = extract_text(file_bytes, filename)
    print("DOCX Text Sample:\n", text[:500])

def test_document_upload_flow():
    from server.app.services.document_processor import process_and_store_document
    from server.app.database import SessionLocal

    BASE_DIR = Path(__file__).resolve().parents[1] 
    file_path = BASE_DIR / "samples" / "customer_interviews.pdf"
    filename = "customer_interviews.pdf"
    file_bytes = file_path.read_bytes()

    db = SessionLocal()
    response = process_and_store_document(
        user_id=1,
        filename="customer_interviews.pdf",
        file_bytes=file_bytes,
        db=db
    )
    assert "document_id" in response
    assert response["num_chunks"] > 0


if __name__ == "__main__":
    test_pdf()
    test_docx()
    test_document_upload_flow()
