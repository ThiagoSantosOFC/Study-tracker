from sqlalchemy import Column, Integer, String
from database.connection import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    permissions = Column(String, nullable=False)