from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    wallet = relationship('Wallet', back_populates='user')


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='wallet')
    history = relationship('WalletHistory', back_populates='wallet')


class WalletHistory(Base):
    __tablename__ = 'wallet_histories'

    id = Column(Integer, primary_key=True)
    operation_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    wallet_id = Column(Integer, ForeignKey('wallets.id'), nullable=False)
    wallet = relationship('Wallet', back_populates='history')


class CustomTax(Base):
    __tablename__ = 'custom_taxes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    default_cost = Column(Float, nullable=False)
    payment_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User')


