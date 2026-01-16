from sqlalchemy import Column,Integer,String,Float,ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "Category"
    id= Column(Integer,primary_key=True,index=True)
    name= Column(String,unique=True,index=True)
    image_url= Column(String)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "Product"
    id= Column(Integer,primary_key=True,index=True)
    name= Column(String)
    price= Column(Float)
    description= Column(String)
    quantity= Column(Integer)
    category_id = Column(Integer, ForeignKey("Category.id"))
    image_url= Column(String)

    category = relationship("Category", back_populates="products")


class User(Base):
    __tablename__ = "User"
    id= Column(Integer,primary_key=True,index=True)
    username= Column(String,unique=True,index=True)
    email= Column(String,unique=True,index=True)
    password= Column(String)
