from sqlalchemy import Column, DateTime, Integer, String, func
import uuid
from sqlalchemy.dialects.postgresql import UUID
from models_new.base import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    workerId = Column(
                    UUID(as_uuid=True),
                    server_default=func.gen_random_uuid(),
                    unique=True,
                    nullable=False

    )
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"