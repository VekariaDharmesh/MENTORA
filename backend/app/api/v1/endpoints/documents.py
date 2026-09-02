from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.deps import get_doc_service
from app.db.session import get_db
from app.db.models import Document, DocumentChunk
from app.services.document_parser import DocumentParserService

router = APIRouter()

@router.post("/documents/upload", tags=["Knowledge Engine"])
async def upload_document(
    file: UploadFile = File(...),
    doc_service: DocumentParserService = Depends(get_doc_service),
    db: Session = Depends(get_db)
):
    """
    Parses, extracts sections, and chunks an uploaded document. Stores in Database.
    """
    content = await file.read()
    
    # Process text & chunks
    parsed = doc_service.process_document(content, filename=file.filename)
    
    # Save Document
    doc_db = Document(
        filename=file.filename,
        file_type=file.filename.split(".")[-1].lower(),
        size_mb=round(len(content) / (1024 * 1024), 2),
        total_chapters=parsed["total_chunks"]
    )
    db.add(doc_db)
    db.commit()
    db.refresh(doc_db)
    
    # Save Chunks
    for chunk in parsed["chunks"]:
        chunk_db = DocumentChunk(
            document_id=doc_db.id,
            content=chunk.text,
            page_number=chunk.page_number,
            section=chunk.section,
            embedding=chunk.embedding
        )
        db.add(chunk_db)
    db.commit()

    return {
        "status": "success",
        "document": {
            "id": doc_db.id,
            "filename": doc_db.filename,
            "file_type": doc_db.file_type,
            "size_mb": doc_db.size_mb,
            "total_chapters": doc_db.total_chapters,
            "last_studied": "Just now",
            "sections": parsed["sections"]
        },
        "total_chunks": parsed["total_chunks"],
        "sections": parsed["sections"]
    }

@router.get("/documents", tags=["Knowledge Engine"])
async def list_documents(db: Session = Depends(get_db)):
    """
    Lists all documents available in the student's material library.
    """
    docs = db.query(Document).all()
    # Also attach sections dynamically from chunks if needed, but for now just basic info
    result = []
    for d in docs:
        sections = db.query(DocumentChunk.section).filter(DocumentChunk.document_id == d.id).distinct().all()
        result.append({
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "size_mb": d.size_mb,
            "total_chapters": d.total_chapters,
            "last_studied": "Recently",
            "sections": [s[0] for s in sections] if sections else ["General"]
        })
    return {"documents": result}
