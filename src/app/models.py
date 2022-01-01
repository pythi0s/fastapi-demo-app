import os
import sys
import datetime

from sqlalchemy.sql.sqltypes import Boolean

from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float

pwd = os.getcwd()
sys.path.append(pwd)


class Item(Base):

    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, unique=False, index=True)
    name = Column(String(50), unique=False, index=True)
    description = Column(String(50), unique=False, index=True)
    manufacturer = Column(String(50), unique=False, index=True)
    category = Column(String(50), unique=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.now())
