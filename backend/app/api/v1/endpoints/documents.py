"""
Documents & Material Library Endpoints
"""

from fastapi import APIRouter, UploadFile, File, Depends
from uuid import uuid4
from typing import List, Dict, Any

from app.core.deps import get_doc_service
from app.services.document_parser import DocumentParserService, SAMPLE_PHYSICS_TEXTBOOK

router = APIRouter()

in_memory_documents = [
    {
        "id": "doc-01",
        "filename": "Electricity & Magnetism.pdf",
        "file_type": "pdf",
        "size_mb": 4.8,
        "total_chapters": 12,
        "last_studied": "Yesterday",
        "sections": ["Electric Charge", "Current", "Voltage", "Resistance", "Ohm's Law"]
    },
    {
        "id": "doc-02",
        "filename": "Machine Learning Fundamentals.pdf",
        "file_type": "pdf",
        "size_mb": 6.2,
        "total_chapters": 8,
        "last_studied": "3 days ago",
        "sections": ["Supervised Learning", "Linear Regression", "Gradient Descent", "Neural Networks"]
    }
]

@router.post("/documents/upload", tags=["Knowledge Engine"])
async def upload_document(
    file: UploadFile = File(...),
    doc_service: DocumentParserService = Depends(get_doc_service)
):
    """
    Parses, extracts sections, and chunks an uploaded document.
    """
    content = await file.read()
    text_content = content.decode("utf-8", errors="ignore")
    if not text_content.strip():
        text_content = SAMPLE_PHYSICS_TEXTBOOK

    parsed = doc_service.parse_text(text_content, filename=file.filename)
    
    doc_record = {
        "id": f"doc-{uuid4().hex[:6]}",
        "filename": file.filename,
        "file_type": file.filename.split(".")[-1].lower(),
        "size_mb": round(len(content) / (1024 * 1024), 2),
        "total_chapters": len(parsed["sections"]),
        "last_studied": "Just now",
        "sections": parsed["sections"]
    }
    in_memory_documents.append(doc_record)

    return {
        "status": "success",
        "document": doc_record,
        "total_chunks": parsed["total_chunks"],
        "sections": parsed["sections"]
    }

@router.get("/documents", tags=["Knowledge Engine"])
async def list_documents():
    """
    Lists all documents available in the student's material library.
    """
    return {"documents": in_memory_documents}
