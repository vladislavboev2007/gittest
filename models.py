from sqlalchemy import Column, Integer, String, Date, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime


# В models.py замените класс Pecent на Percent
class Percent(Base):
    __tablename__ = "percent"  # Изменили с "pecent" на "percent"

    idpercent = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ts = Column(Date, nullable=False)
    rate = Column(DECIMAL(2, 2), nullable=False)


class Products(Base):
    __tablename__ = "products"

    idproducts = Column('idproducts', Integer, primary_key=True, index=True)
    title = Column('title', String(45), nullable=False)
    descriptions = Column('descriptions', String(255), default="Not description.")


class Profit(Base):
    __tablename__ = "profit"

    idprofit = Column('idprofit', Integer, primary_key=True, index=True, autoincrement=True)
    ts = Column('ts', DateTime, nullable=False)
    idregister = Column('idregister', Integer, nullable=False)
    quantice = Column('quantice', Integer, nullable=False)
    price = Column('price', DECIMAL(10, 2), nullable=False)
    total = Column('total', DECIMAL(10, 2), nullable=False)
    n_profit = Column('n_profit', DECIMAL(10, 2), nullable=False)
    rate = Column('rate', DECIMAL(2, 2), nullable=False)


class Register(Base):
    __tablename__ = "register"

    idregister = Column('idregister', Integer, primary_key=True, index=True, autoincrement=True)
    ts = Column('ts', DateTime, nullable=False)
    product = Column('product', Integer, ForeignKey('products.idproducts'), nullable=False)
    quantite = Column('quantite', Integer, nullable=False)
    price = Column('price', DECIMAL(10, 2), nullable=False)
    total = Column('total', DECIMAL(10, 2), nullable=False)
    n_total = Column('n_total', DECIMAL(10, 2))
    n_quantite = Column('n_quantite', Integer)
    n_price = Column('n_price', DECIMAL(10, 2))

    product_rel = relationship("Products")