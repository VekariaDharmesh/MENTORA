with open("backend/app/db/models.py", "r") as f:
    content = f.read()

new_class = """class MediaJob(Base):
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
"""

old_class = """class MediaJob(Base):
    __tablename__ = "media_jobs"
    id = Column(String, primary_key=True, default=generate_uuid)
    segment_id = Column(String, ForeignKey("lesson_segments.id"), nullable=True)
    status = Column(String, default="QUEUED")
    stage = Column(String, default="SCRIPT")
    progress = Column(Integer, default=0)
    audio_url = Column(String, nullable=True)
    visual_url = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)"""

content = content.replace(old_class, new_class)

with open("backend/app/db/models.py", "w") as f:
    f.write(content)
