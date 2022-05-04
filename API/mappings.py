

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class User(Base):
   __tablename__ = 'user'

   id = Column(Integer, primary_key=True)
   username = Column(String, unique=True, nullable=False)
   email = Column(String, nullable=False)
   password = Column(String, nullable=False)
   register_data = Column(DateTime(timezone=True))
