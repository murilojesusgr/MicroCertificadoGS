from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Certificate(Base):
    __tablename__ = 'certificates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    course = Column(String, nullable=False)
    date_issued = Column(Date, nullable=False)
    pdf_path = Column(String, nullable=True)
