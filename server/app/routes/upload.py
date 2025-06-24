# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.auth import get_current_user
from app.services.document_processor import process_and_store_document
from ..database import SessionLocal

router = APIRouter(prefix="/upload", tags=["Documents"])

@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    if not file.filename.endswith((".txt", ".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    db = SessionLocal()
    contents = await file.read()
    process_and_store_document(user.id, file.filename, contents, db=db)
    return {"message": "Upload successful"}
