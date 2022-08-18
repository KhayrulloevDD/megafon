from sqlalchemy import Column, Integer, String

from dbs.sqlite import Base
from dbs.postgresql import Base as pg_Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String)
    amount = Column(Integer)
    description = Column(String)


class PGPayment(pg_Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String)
    amount = Column(Integer)
    description = Column(String)
