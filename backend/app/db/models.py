import datetime
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True)
    is_guest = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="user", uselist=False)


class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    display_name = Column(String, default="Learner")
    learning_level = Column(String, default="beginner")
    default_language = Column(String, default="English")
    learning_style = Column(String, default="example_first")
    learning_goal = Column(Text, nullable=True)
    total_learning_time_seconds = Column(Integer, default=0)

    user = relationship("User", back_populates="profile")
    mastery_records = relationship("ConceptMastery", back_populates="student")
    lessons = relationship("Lesson", back_populates="student")


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=generate_uuid)
    student_id = Column(String, ForeignKey("student_profiles.id"), nullable=True)
    filename = Column(String)
    file_type = Column(String)
    size_mb = Column(Float)
    total_chapters = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(String, primary_key=True, default=generate_uuid)
    document_id = Column(String, ForeignKey("documents.id"))
    content = Column(Text)
    page_number = Column(Integer, nullable=True)
    chapter = Column(String, nullable=True)
    section = Column(String, nullable=True)
    concept = Column(String, nullable=True)
    embedding = Column(JSON, nullable=True)
    
    document = relationship("Document", back_populates="chunks")


class Concept(Base):
    __tablename__ = "concepts"
    id = Column(String, primary_key=True, default=generate_uuid)
    key = Column(String, unique=True, index=True)
    name = Column(String)
    domain = Column(String)
    description = Column(Text)
    difficulty_level = Column(String, default="beginner")


class ConceptRelationship(Base):
    __tablename__ = "concept_relationships"
    id = Column(String, primary_key=True, default=generate_uuid)
    concept_id = Column(String, ForeignKey("concepts.id"))
    prerequisite_id = Column(String, ForeignKey("concepts.id"))


class ConceptMastery(Base):
    __tablename__ = "concept_mastery"
    id = Column(String, primary_key=True, default=generate_uuid)
    student_id = Column(String, ForeignKey("student_profiles.id"))
    concept_id = Column(String, ForeignKey("concepts.id"))
    mastery_score = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.0)
    attempts_count = Column(Integer, default=0)
    successful_attempts = Column(Integer, default=0)
    
    student = relationship("StudentProfile", back_populates="mastery_records")
    concept = relationship("Concept")


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(String, primary_key=True, default=generate_uuid)
    student_id = Column(String, ForeignKey("student_profiles.id"))
    topic = Column(String)
    target_duration_minutes = Column(Integer)
    language = Column(String)
    level = Column(String)
    objective = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("StudentProfile", back_populates="lessons")
    segments = relationship("LessonSegment", back_populates="lesson", cascade="all, delete-orphan", order_by="LessonSegment.sequence")


class LessonSegment(Base):
    __tablename__ = "lesson_segments"
    id = Column(String, primary_key=True, default=generate_uuid)
    lesson_id = Column(String, ForeignKey("lessons.id"))
    sequence = Column(Integer)
    concept_id = Column(String, ForeignKey("concepts.id"), nullable=True)
    concept_name = Column(String)
    duration = Column(Integer)
    strategy = Column(String)
    visual_type = Column(String)
    caption = Column(Text)
    has_checkpoint = Column(Boolean, default=False)
    
    lesson = relationship("Lesson", back_populates="segments")


class TeachingSession(Base):
    __tablename__ = "teaching_sessions"
    id = Column(String, primary_key=True, default=generate_uuid)
    lesson_id = Column(String, ForeignKey("lessons.id"))
    student_id = Column(String, ForeignKey("student_profiles.id"))
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="IN_PROGRESS") # IN_PROGRESS, COMPLETED


class TeachingEvent(Base):
    __tablename__ = "teaching_events"
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey("teaching_sessions.id"))
    segment_id = Column(String, ForeignKey("lesson_segments.id"), nullable=True)
    event_type = Column(String) # EXPLAIN, QUESTION, ADAPT
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    payload = Column(JSON, nullable=True)


class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, default=generate_uuid)
    concept_id = Column(String, ForeignKey("concepts.id"))
    prompt = Column(Text)
    options = Column(JSON) # e.g. {"A": "...", "B": "..."}
    correct_option = Column(String)
    difficulty = Column(String)


class StudentResponse(Base):
    __tablename__ = "student_responses"
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey("teaching_sessions.id"))
    question_id = Column(String, ForeignKey("questions.id"))
    student_answer = Column(String)
    is_correct = Column(Boolean)
    misconception_detected = Column(String, nullable=True)


class MediaJob(Base):
    __tablename__ = "media_jobs"
    id = Column(String, primary_key=True, default=generate_uuid)
    lesson_id = Column(String, nullable=True)
    segment_id = Column(String, ForeignKey("lesson_segments.id"), nullable=True)
    provider = Column(String, default="heygen")
    provider_job_id = Column(String, nullable=True)
    status = Column(String, default="QUEUED")
    stage = Column(String, default="SCRIPT")
    progress = Column(Integer, default=0)
    audio_url = Column(String, nullable=True)
    visual_url = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)


