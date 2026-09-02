"""
Concept Graph & Prerequisite Endpoints
"""

from fastapi import APIRouter, Depends
from app.core.deps import get_concept_service
from app.services.concept_graph import ConceptGraphService

router = APIRouter()

@router.get("/concepts/graph", tags=["Concept Graph"])
async def get_concept_graph(
    concept_service: ConceptGraphService = Depends(get_concept_service)
):
    """
    Returns the directed concept graph and prerequisite relations.
    """
    return concept_service.get_graph()
