"""
Core Dependencies & Service Singletons
Provides Dependency Injection (DI) singletons for the FastAPI application layer.
"""

from app.services.document_parser import DocumentParserService
from app.services.concept_graph import ConceptGraphService
from app.services.learner_model import LearnerModelService
from app.services.visual_engine import VisualEngineService
from app.services.multilingual_engine import MultilingualEngineService
from app.services.media_engine import MediaEngineService
from app.services.assessment_engine import AssessmentEngineService
from app.services.advanced_features import AdvancedFeaturesService
from app.services.production_support import ProductionSupportService
from app.services.llm_service import LLMService
from app.teaching.state_machine import TeachingStateMachine

# Singleton service instances
llm_service = LLMService()
doc_service = DocumentParserService()
concept_service = ConceptGraphService()
learner_service = LearnerModelService()
visual_service = VisualEngineService()
multilingual_service = MultilingualEngineService()
media_service = MediaEngineService()
assessment_service = AssessmentEngineService(llm_service)
advanced_service = AdvancedFeaturesService()
support_service = ProductionSupportService()
teaching_machine = TeachingStateMachine(llm_service)

def get_llm_service() -> LLMService:
    return llm_service

def get_doc_service() -> DocumentParserService:
    return doc_service

def get_concept_service() -> ConceptGraphService:
    return concept_service

def get_learner_service() -> LearnerModelService:
    return learner_service

def get_visual_service() -> VisualEngineService:
    return visual_service

def get_multilingual_service() -> MultilingualEngineService:
    return multilingual_service

def get_media_service() -> MediaEngineService:
    return media_service

def get_assessment_service() -> AssessmentEngineService:
    return assessment_service

def get_advanced_service() -> AdvancedFeaturesService:
    return advanced_service

def get_support_service() -> ProductionSupportService:
    return support_service

def get_teaching_machine() -> TeachingStateMachine:
    return teaching_machine
from app.services.vector_search import VectorSearchService
vector_search_service = VectorSearchService()
def get_vector_search() -> VectorSearchService:
    return vector_search_service
