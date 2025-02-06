# ===================== DATABASE MODEL =====================
# models/twosum_result.py
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

e = create_engine(DATABASE_URL)
Session = sessionmaker(bind=e)

class TwoSumResult(Base):
    __tablename__ = "two_sum_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    target = Column(Integer, nullable=False)

Base.metadata.create_all(e)
