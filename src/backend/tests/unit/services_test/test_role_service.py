import pytest
from datetime import datetime, timezone
from services.role_service import RoleService
from exceptions import RoleNotFoundException, InvalidDataException, UnauthorizedAccessError
from database.models.role import Role
from database.models.user import User

def generate_role_data(suffix: str = "") -> dict:
    current_time = datetime.now(timezone.utc)
    return {
        "name": f"test_role_{suffix}",
        "description": f"Test Role Description {suffix}",
        "permissions": ["read", "write"],
        "is_active": True,
        "created_at": current_time,
        "updated_at": current_time
    }

@pytest.fixture
def role_service(db_session):
    service = RoleService(db_session)
    service._verify_admin_access = lambda x: True
    return service

@pytest.fixture
def admin_role(db_session):
    current_time = datetime.now(timezone.utc)
    admin_role = Role(
        name="test_admin",
        description="Test Admin Role",
        permissions=["admin"],
        created_at=current_time,
        updated_at=current_time,
        is_active=True
    )
    db_session.add(admin_role)
    db_session.commit()
    return admin_role

@pytest.fixture
def admin_user(db_session, admin_role):
    current_time = datetime.now(timezone.utc)
    admin = User(
        username="admin",
        email="admin@test.com",
        password="hashed_password",
        is_active=True,
        role_id=admin_role.id,
        created_at=current_time,
        updated_at=current_time
    )
    db_session.add(admin)
    db_session.commit()
    return admin

@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    db_session.query(User).delete()
    db_session.query(Role).delete()
    db_session.commit()
    yield
    db_session.query(User).delete()
    db_session.query(Role).delete()
    db_session.commit()

class TestRoleService:
    def test_create_role_success(self, role_service):
        role_data = generate_role_data("1")
        role = role_service.create_role(role_data, requesting_user_id=1)
        
        assert role is not None
        assert role.name == role_data["name"]
        assert role.description == role_data["description"]
        assert role.permissions == role_data["permissions"]
        assert role.is_active

    def test_create_role_invalid_data(self, role_service):
        invalid_data = {
            "name": "",
            "description": "Test Description"
        }
        with pytest.raises(InvalidDataException):
            role_service.create_role(invalid_data, requesting_user_id=1)

    def test_create_system_role_unauthorized(self, role_service):
        system_role_data = generate_role_data()
        system_role_data["name"] = "admin"
        with pytest.raises(UnauthorizedAccessError):
            role_service.create_role(system_role_data, requesting_user_id=1)

    def test_get_role_success(self, role_service):
        role_data = generate_role_data("2")
        created_role = role_service.create_role(role_data, requesting_user_id=1)
        
        retrieved_role = role_service.get_role(created_role.id, requesting_user_id=1)
        assert retrieved_role is not None
        assert retrieved_role.name == role_data["name"]
        assert retrieved_role.description == role_data["description"]

    def test_get_nonexistent_role(self, role_service):
        with pytest.raises(RoleNotFoundException):
            role_service.get_role(999, requesting_user_id=1)

    def test_update_role_success(self, role_service):
        role_data = generate_role_data("3")
        role = role_service.create_role(role_data, requesting_user_id=1)
        
        update_data = {
            "name": "Updated Role Name",
            "description": "Updated Description"
        }
        updated_role = role_service.update_role(role.id, update_data, requesting_user_id=1)
        
        assert updated_role.name == update_data["name"]
        assert updated_role.description == update_data["description"]

    def test_update_system_role_unauthorized(self, role_service):
        role_data = generate_role_data("system")
        role = role_service.create_role(role_data, requesting_user_id=1)
        
        update_data = {"name": "admin"}
        with pytest.raises(UnauthorizedAccessError) as exc:
            role_service.update_role(role.id, update_data, requesting_user_id=1)
        assert "Cannot modify role to be a system role" in str(exc.value)

    def test_delete_role_success(self, role_service, db_session):
        role_data = generate_role_data("4")
        role = role_service.create_role(role_data, requesting_user_id=1)
        role_id = role.id
        
        assert role_service.delete_role(role_id, requesting_user_id=1) is True
        
        db_session.expire_all()
        
        with pytest.raises(RoleNotFoundException):
            role_service.get_role(role_id, requesting_user_id=1)

    def test_delete_system_role_unauthorized(self, role_service):
        role_data = generate_role_data("system")
        role = role_service.create_role(role_data, requesting_user_id=1)
        
        update_data = {"name": "admin"}
        with pytest.raises(UnauthorizedAccessError) as exc:
            role_service.update_role(role.id, update_data, requesting_user_id=1)
        assert "Cannot modify role to be a system role" in str(exc.value)