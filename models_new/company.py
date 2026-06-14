from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship
from models_new.base import Base


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=True)
    user = relationship('user', backref='clients')
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"