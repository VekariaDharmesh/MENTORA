-- ============================================================================
-- AI TEACHER — POSTGRESQL + PGVECTOR DATABASE SCHEMA
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ----------------------------------------------------------------------------
-- 1. USERS & STUDENTS
-- ----------------------------------------------------------------------------
CREATE TYPE user_role_enum AS ENUM ('student', 'educator', 'admin');
CREATE TYPE learning_level_enum AS ENUM ('beginner', 'intermediate', 'advanced');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255),
    is_guest BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    display_name VARCHAR(100) NOT NULL DEFAULT 'Learner',
    default_language VARCHAR(20) NOT NULL DEFAULT 'Hinglish',
    learning_level learning_level_enum NOT NULL DEFAULT 'beginner',
    learning_goal VARCHAR(255),
    total_learning_time_seconds INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE student_preferences (
    student_id UUID PRIMARY KEY REFERENCES students(id) ON DELETE CASCADE,
    teacher_personality VARCHAR(50) DEFAULT 'Socratic',
    voice_preference VARCHAR(50) DEFAULT 'Natural Female',
    avatar_model VARCHAR(50) DEFAULT 'Dr. Aris',
    captions_enabled BOOLEAN DEFAULT TRUE,
    reduced_motion BOOLEAN DEFAULT FALSE,
    sound_effects_enabled BOOLEAN DEFAULT TRUE
);

-- ----------------------------------------------------------------------------
-- 2. KNOWLEDGE ENGINE: DOCUMENTS, SECTIONS & VECTOR CHUNKS
-- ----------------------------------------------------------------------------
CREATE TYPE document_status_enum AS ENUM ('uploaded', 'parsing', 'embedded', 'failed');

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(20) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    storage_path VARCHAR(512) NOT NULL,
    status document_status_enum DEFAULT 'uploaded',
    extracted_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    chapter_number INTEGER,
    page_start INTEGER,
    page_end INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    section_id UUID REFERENCES document_sections(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    page_number INTEGER,
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chunks_embedding ON document_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ----------------------------------------------------------------------------
-- 3. CONCEPT GRAPH & PREREQUISITES
-- ----------------------------------------------------------------------------
CREATE TABLE concepts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    description TEXT,
    difficulty_level learning_level_enum DEFAULT 'beginner',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE concept_prerequisites (
    concept_id UUID REFERENCES concepts(id) ON DELETE CASCADE,
    prerequisite_id UUID REFERENCES concepts(id) ON DELETE CASCADE,
    PRIMARY KEY (concept_id, prerequisite_id)
);

CREATE TABLE concept_sources (
    concept_id UUID REFERENCES concepts(id) ON DELETE CASCADE,
    document_chunk_id UUID REFERENCES document_chunks(id) ON DELETE CASCADE,
    PRIMARY KEY (concept_id, document_chunk_id)
);

-- ----------------------------------------------------------------------------
-- 4. STUDENT MASTERY & MISCONCEPTIONS
-- ----------------------------------------------------------------------------
CREATE TYPE misconception_category_enum AS ENUM (
    'definition_error',
    'formula_error',
    'concept_reversal',
    'cause_effect_error',
    'prerequisite_gap',
    'application_error'
);

CREATE TABLE student_concept_mastery (
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    concept_id UUID REFERENCES concepts(id) ON DELETE CASCADE,
    mastery_score FLOAT NOT NULL DEFAULT 0.0 CHECK (mastery_score >= 0.0 AND mastery_score <= 1.0),
    confidence_score FLOAT NOT NULL DEFAULT 0.0 CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    attempts_count INTEGER DEFAULT 0,
    successful_attempts INTEGER DEFAULT 0,
    last_studied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, concept_id)
);

CREATE TABLE student_misconceptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    concept_id UUID REFERENCES concepts(id) ON DELETE CASCADE,
    category misconception_category_enum NOT NULL,
    detected_statement TEXT NOT NULL,
    teacher_observation TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- ----------------------------------------------------------------------------
-- 5. LESSONS, SEGMENTS & CHECKPOINTS
-- ----------------------------------------------------------------------------
CREATE TYPE teaching_state_enum AS ENUM (
    'init', 'understand', 'plan', 'introduce', 'explain', 
    'demonstrate', 'question', 'evaluate', 'remediate', 'complete'
);

CREATE TYPE visual_type_enum AS ENUM (
    'circuit', 'water_pipe', 'equation', 'graph', 'diagram', 'code', 'table'
);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    topic VARCHAR(255) NOT NULL,
    target_duration_minutes INTEGER NOT NULL DEFAULT 20,
    language VARCHAR(30) NOT NULL DEFAULT 'Hinglish',
    level learning_level_enum NOT NULL DEFAULT 'beginner',
    learning_objective TEXT,
    overall_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lesson_segments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lesson_id UUID REFERENCES lessons(id) ON DELETE CASCADE,
    concept_id UUID REFERENCES concepts(id) ON DELETE SET NULL,
    sequence_order INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    strategy VARCHAR(50) NOT NULL,
    visual_type visual_type_enum NOT NULL,
    script_text TEXT NOT NULL,
    audio_url VARCHAR(512),
    avatar_video_url VARCHAR(512),
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE checkpoints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    segment_id UUID REFERENCES lesson_segments(id) ON DELETE CASCADE,
    question_prompt TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option CHAR(1) NOT NULL,
    explanation TEXT NOT NULL
);

CREATE TABLE student_checkpoint_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    checkpoint_id UUID REFERENCES checkpoints(id) ON DELETE CASCADE,
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    selected_option CHAR(1) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    diagnosed_misconception_id UUID REFERENCES student_misconceptions(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
