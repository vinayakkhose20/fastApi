from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from database import session,engine
from models import Product,User,Category
import database_model
from sqlalchemy.orm import Session


#create all tabels listed in database_model.py
database_model.Base.metadata.create_all(bind=engine)

app=FastAPI()

#allow react to interact apis
#allow method to access outside in react
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)



def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def welcome():
     return "welcome to bakend "

@app.get("/categories")
def get_categorys(db:Session=Depends(get_db)):
      cats=db.query(database_model.Category).all()
      return cats

@app.post("/categories")
def add_category(category: Category, db: Session = Depends(get_db)):
    db_category = database_model.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    return db_category

@app.put("/categories/{id}")
def update_category(id: int, category: Category, db: Session = Depends(get_db)):
     db_category = db.query(database_model.Category).filter(database_model.Category.id==id).first()
     if db_category:
          db_category.name= category.name
          db_category.image_url= category.image_url
          db.commit()
          return "category updated"
     return "category not found"

@app.delete("/categories/{id}")
def delete_category(id: int, db:Session=Depends(get_db)):
     cat = db.query(database_model.Category).filter(database_model.Category.id==id).first()
     if cat:
          db.delete(cat)
          db.commit()
          return "product delete"
     return "product not found"

    


#getting all products
@app.get("/products")
def get_products(db:Session=Depends(get_db)):
      prods=db.query(database_model.Product).all()
      return prods



#updating product base on id
@app.get("/products/{id}")
def get_data(id:int,db:Session=Depends(get_db)):
      prod=db.query(database_model.Product).filter(database_model.Product.id==id).first()
      if prod:
          return prod
      return "product not found"


#adding product 
@app.post("/products")
def add_product(prod:Product,db:Session=Depends(get_db)):
    #firstly check that category id is available or not
    cat=db.query(database_model.Category).filter(database_model.Category.id==prod.category_id).first()
    if cat:
      db.add(database_model.Product(**prod.model_dump()))
      db.commit()
      return prod
    return "category of product not avalable"



#updating product base on id
@app.put("/products/{id}")
def update_product(id:int,products:Product,db:Session=Depends(get_db)):
    prod=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    data=db.query(database_model.Category).filter(database_model.Category.id==products.category_id).first()
    if prod and data :
        prod.name=products.name
        prod.price=products.price
        prod.description=products.description
        prod.quantity=products.quantity
        prod.category_id = products.category_id
        prod.image_url=products.image_url
        db.commit()
        return "product updated"
    return "product not found"


@app.delete("/products/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
      prod=db.query(database_model.Product).filter(database_model.Product.id==id).first()
      if prod:
          db.delete(prod)
          db.commit()
          return "product deleted"
      return "product not found"


# user table
@app.get("/users/")
def get_user(db:Session=Depends(get_db)):
       return db.query(database_model.User).all()
       
@app.get("/users/{id}")
def get_user_by_id(id:int,db:Session=Depends(get_db)):
     user=db.query(database_model.User).filter(database_model.User.id==id).first()
     if user:
          return user
     return "user not found"


@app.post("/users")
def add_users(user:User,db:Session=Depends(get_db)):
     res=db.query(database_model.User).filter(database_model.User.email==user.email).first()
     if not res:
       db.add(database_model.User(**user.model_dump()))
       db.commit()
       return "user added"
     return "Email Alredy Register"

@app.put("/users/{id}")
def update_user(id:int,user:User,db:Session=Depends(get_db)):
     users=db.query(database_model.User).filter(database_model.User.id==id).first()
     if users:
          users.username=user.username
          users.email=user.email
          users.password=user.password
          db.commit()
          return "user updated"
     return "user not found"


@app.delete("/users/{id}")
def delete_user(id:int,db:Session=Depends(get_db)):
     user=db.query(database_model.User).filter(database_model.User.id==id).first()
     if user:
          db.delete(user)
          db.commit()
          return "user deleted"
     return "user not found"

