from sqlalchemy import create_engine, Column, String, Boolean, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    
    token = Column(String(85), primary_key=True)
    is_banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    last_check = Column(DateTime)

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    type = Column(String(20)) 
    url = Column(String(500))
    parameters = Column(JSON) 
    status = Column(String(20), default='pending')  
    next_run = Column(DateTime)
    interval = Column(Integer)  
    created_at = Column(DateTime, default=datetime.now)

engine = create_engine('sqlite:///accounts.db')
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)