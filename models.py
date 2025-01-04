from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserChoice(Base):
    __tablename__ = "user_choices"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    number_of_classes = Column(Integer, default=None)
    color = Column(String, default=None)
    type_of_mark = Column(String, default=None)
    cost_for_apply = Column(String, default=None)
    cost_for_publication = Column(String, default=None)
    cost_for_search = Column(String, default=None)
    date_of_creation = Column(DateTime, default=datetime.now())
