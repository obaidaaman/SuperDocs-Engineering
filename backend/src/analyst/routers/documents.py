from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from ..ingestion.parser import parse_pdf_document, compute_sha256

router = APIRouter(prefix="/documents", tags=["documents"])

STORAGE_DIR = os.path.join(os.getcwd(), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for now.")
    
    # Save the file temporarily to compute hash
    temp_path = os.path.join(STORAGE_DIR, f"temp_{file.filename}")
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_hash = compute_sha256(temp_path)
    
    # Check if we already have it
    final_path = os.path.join(STORAGE_DIR, f"{file_hash}.pdf")
    if os.path.exists(final_path):
        os.remove(temp_path)
        return {"message": "File already exists", "file_hash": file_hash}
        
    # Move to final destination
    os.rename(temp_path, final_path)
    
    # Run parsing pipeline
    try:
        blocks = parse_pdf_document(final_path)
        return {
            "message": "File processed successfully",
            "file_hash": file_hash,
            "filename": file.filename,
            "blocks_extracted": len(blocks),
            "preview": blocks[:2] if blocks else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing document: {str(e)}")
