from datetime import datetime, timezone
from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator
from typing import Optional, Dict, Any
from exceptions import TaskNotFoundException, InvalidDataException, UnauthorizedAccessError
from repositories.task_repository import TaskRepository
from sqlalchemy.orm import Session
import logging
from database.models.task import Task 

logger = logging.getLogger(__name__)

class TaskCreate(BaseModel):
    """Validation model for creating tasks"""
    title: str = Field(
        title="Task Title",
        description="The title of the task",
        min_length=1,
        max_length=200
    )
    description: str = Field(
        title="Task Description",
        description="Detailed description of the task",
        min_length=1
    )
    due_date: Optional[datetime] = Field(
        default=None,
        title="Due Date",
        description="When the task is due"
    )
    priority_level: str = Field(
        default="medium",
        title="Priority Level",
        description="Task priority level (low/medium/high)"
    )
    task_status: str = Field(
        default="pending",
        title="Task Status",
        description="Current status of the task"
    )
    created_by_user_id: int = Field(
        title="Creator ID",
        description="ID of the user creating the task"
    )
    created_at_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Creation Time"
    )
    last_updated_at_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Last Update Time"
    )

    @field_validator('priority_level')
    def validate_task_priority(cls, priority_level: str) -> str:
        allowed_priorities = ['low', 'medium', 'high']
        normalized_priority = priority_level.lower()
        if normalized_priority not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}")
        return normalized_priority

    @field_validator('task_status')
    def validate_task_status(cls, task_status: str) -> str:
        allowed_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        normalized_status = task_status.lower()
        if normalized_status not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return normalized_status

    @field_validator('due_date')
    def validate_task_due_date(cls, due_date: Optional[datetime]) -> Optional[datetime]:
        if due_date and due_date <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return due_date

class TaskService:

    def __init__(self, database_session: Session):
        if not isinstance(database_session, Session):
            raise ValueError("Invalid database session provided")
        self.database_session = database_session
        self.task_repository = TaskRepository(database_session)

    def verify_user_task_access(self, task: Task, requesting_user_id: int) -> None:
        """Verify if user has access to the task"""
        if not task or task.created_by_user_id != requesting_user_id:
            raise UnauthorizedAccessError("User not authorized to access this task")

    def get_task_by_id(self, task_id: int, requesting_user_id: int) -> Task:
        """Get a task by ID with user authorization check"""
        try:
            task = self.task_repository.get_task_by_id(task_id)
            if not task:
                raise TaskNotFoundException(f"Task {task_id} not found")
            
            self.verify_user_task_access(task, requesting_user_id)
            return task
        except Exception as error:
            logger.error(f"Error retrieving task {task_id}: {str(error)}")
            raise

    def create_new_task(self, task_data: Dict[str, Any], requesting_user_id: int) -> Task:
        """Create a new task with validation"""
        try:
            if not requesting_user_id:
                raise UnauthorizedAccessError("User ID is required to create a task")

            # Set creation metadata
            current_time = datetime.now(timezone.utc)
            task_data.update({
                'created_by_user_id': requesting_user_id,
                'created_at_utc': current_time,
                'last_updated_at_utc': current_time
            })

            # Validate task data
            validated_task = TaskCreate(**task_data)
            
            # Create task in repository
            created_task = self.task_repository.create_task(
                validated_task.model_dump(exclude_unset=True)
            )
            
            if not created_task:
                raise InvalidDataException("Failed to create task")
            
            return created_task

        except ValueError as error:
            logger.warning(
                f"Validation error creating task for user {requesting_user_id}: {str(error)}"
            )
            raise InvalidDataException(str(error))
        except Exception as error:
            logger.error(
                f"Error creating task for user {requesting_user_id}: {str(error)}"
            )
            raise
    
    def update_existing_task(
        self, 
        task_id: int, 
        update_data: Dict[str, Any], 
        requesting_user_id: int
    ) -> Dict[str, Any]:
        try:
            existing_task = self.get_task_by_id(task_id, requesting_user_id)
        
            update_data.pop('created_by_user_id', None)
            update_data.pop('created_at_utc', None)

            update_data['last_updated_at_utc'] = datetime.now(timezone.utc)
            
            updated_task = self.task_repository.update_task(task_id, update_data)
            if not updated_task:
                raise TaskNotFoundException(f"Task {task_id} not found")
            
            return updated_task
        except Exception as error:
            logger.error(f"Error updating task {task_id}: {str(error)}")
            raise

    def delete_task_by_id(self, task_id: int, requesting_user_id: int) -> bool:
        try:
            self.verify_user_task_access(
                self.get_task_by_id(task_id, requesting_user_id),
                requesting_user_id
            )
            
            if not self.task_repository.delete_taskById(task_id):
                raise TaskNotFoundException(f"Task {task_id} not found")
            
            logger.info(f"Task {task_id} successfully deleted by user {requesting_user_id}")
            return True
        except Exception as error:
            logger.error(f"Error deleting task {task_id}: {str(error)}")
            raise