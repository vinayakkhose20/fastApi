from pydantic import BaseModel

#inserting data without id
class Category(BaseModel):
    name:str
    image_url :str

class Product(BaseModel):
    name:str
    price:float
    description:str
    quantity:int
    category_id:int
    image_url :str

class User(BaseModel):
    username:str
    email:str
    password:str
