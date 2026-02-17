from sqlalchemy import Column, Integer, String, ForeignKey #foregin key????
from .database import Base

class User(Base):
    __tablename__ = "users_logs"
    id= Column(Integer, primary_key = True, index = True)
    username = Column(String, unique=True, index = True)
    name= Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    age = Column(Integer)


class StudyLog(Base):
    __tablename__ = "study_logs"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users_logs.id"))
    url = Column(String)
    category = Column(String) 
   