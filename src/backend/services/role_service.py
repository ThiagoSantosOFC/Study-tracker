from datetime import datetime, timezone
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Dict, Any
from exceptions import RoleNotFoundException, InvalidDataException, UnauthorizedAccessError
from repositories.role_repository import RoleRepository
from sqlalchemy.orm import Session
import logging
from database.models import Role

logger = logging.getLogger(__name__)

class RoleCreate(BaseModel):
    name: str = Field(
        title="Role Name",
        description="Name of the role",
        min_length=1,
        max_length=100
    )
    description: str = Field(
        title="Role Description",
        description="Description of role permissions and responsibilities",
        min_length=1,
        max_length=500
    )
    permissions: list[str] = Field(
        title="Permissions",
        description="List of permissions granted to this role",
        default=[]
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Creation Time"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Last Update Time"
    )
    is_active: bool = Field(
        default=True,
        title="Active Status"
    )

    @property
    def is_system_role(self) -> bool:
        system_roles = {'admin', 'system', 'superuser'}
        return self.name.lower() in system_roles

class RoleService:
    def __init__(self, database_session: Session):
        if not isinstance(database_session, Session):
            raise ValueError("Invalid database session provided")
        self.database_session = database_session
        self.role_repository = RoleRepository(database_session)

    def _verify_admin_access(self, user_id: int) -> None:
        pass

    def get_role(self, role_id: int, requesting_user_id: int) -> Dict[str, Any]:
        try:
            role = self.role_repository.get_role_by_id(role_id)
            if not role:
                raise RoleNotFoundException(f"Role {role_id} not found")
            return role
        except Exception as error:
            logger.error(f"Error retrieving role {role_id}: {str(error)}")
            raise

    def create_role(
        self, 
        role_data: Dict[str, Any], 
        requesting_user_id: int
    ) -> Dict[str, Any]:
        try:
            self._verify_admin_access(requesting_user_id)
            role_create = RoleCreate(**role_data)

            if role_create.is_system_role:
                logger.warning(f"Attempt to create system role by user {requesting_user_id}")
                raise UnauthorizedAccessError("Cannot create system-level roles")

            created_role = self.role_repository.create_role(
                role_create.model_dump(exclude_unset=True)
            )

            logger.info(f"Role created: {created_role.name} by user {requesting_user_id}")
            return created_role

        except ValidationError as error:
            logger.warning(f"Invalid role data: {str(error)}")
            raise InvalidDataException(str(error))
        except Exception as error:
            logger.error(f"Error creating role: {str(error)}")
            raise

    def update_role(self, role_id: int, role_data: Dict[str, Any], requesting_user_id: int) -> Role:
        try:
            self._verify_admin_access(requesting_user_id)

            existing_role = self.get_role(role_id, requesting_user_id)
            if not existing_role:
                raise RoleNotFoundException(f"Role {role_id} not found")

            # Prevent updating existing system roles
            if existing_role.name.lower() in {'admin', 'system', 'superuser'}:
                raise UnauthorizedAccessError("Cannot modify system roles")

            # Prevent updating to system role names
            if role_data.get('name', '').lower() in {'admin', 'system', 'superuser'}:
                raise UnauthorizedAccessError("Cannot modify role to be a system role")

            role_data['updated_at'] = datetime.now(timezone.utc)
            updated_role = self.role_repository.update_role(role_id, role_data)
            return updated_role

        except Exception as error:
            logger.error(f"Error updating role {role_id}: {str(error)}")
            raise

    def delete_role(self, role_id: int, requesting_user_id: int) -> bool:
        try:
            self._verify_admin_access(requesting_user_id)
            
            existing_role = self.get_role(role_id, requesting_user_id)
            if not existing_role:
                raise RoleNotFoundException(f"Role {role_id} not found")

            if existing_role.name.lower() in {'admin', 'system', 'superuser'}:
                raise UnauthorizedAccessError("Cannot delete system roles")

            if not self.role_repository.delete_role(role_id):
                raise RoleNotFoundException(f"Role {role_id} not found")

            deleted_role = self.role_repository.get_role_by_id(role_id)
            if deleted_role:
                raise Exception("Role deletion failed")

            return True

        except Exception as error:
            logger.error(f"Error deleting role {role_id}: {str(error)}")
            raise