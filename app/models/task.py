from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.models.base import BaseModel

class TaskStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class Project(BaseModel):
    __tablename__ = "projects"
    
    # Project details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Dates
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Foreign keys
    client_id = Column(ForeignKey("clients.id"), nullable=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    client = relationship("Client", back_populates="projects")
    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(BaseModel):
    __tablename__ = "tasks"
    
    # Task details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Status and priority
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.NOT_STARTED)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.NORMAL)
    
    # Dates
    start_date = Column(DateTime)
    due_date = Column(DateTime)
    completed_date = Column(DateTime)
    
    # Foreign keys
    project_id = Column(ForeignKey("projects.id"), nullable=True)
    client_id = Column(ForeignKey("clients.id"), nullable=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(ForeignKey("users.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    client = relationship("Client", back_populates="tasks")
    user = relationship("User", back_populates="tasks", foreign_keys=[user_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
