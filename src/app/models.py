from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    accounts = relationship("Account", backref="customer", lazy="dynamic")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    account_number = Column(String(20), nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    is_blocked = Column(Boolean, default=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
