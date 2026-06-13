from sqlalchemy import Column, DateTime, Integer, String, func
from models_new.base import Base


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"