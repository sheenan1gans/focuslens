from sqlalchemy import Column, Integer, String 
from .database import Base

class StudyLog(Base):
    __tablename__ = "study_logs"
    id = Column(Integer, primary_key = True, index = True)
    url = Column(String)
    category = Column(String) 

