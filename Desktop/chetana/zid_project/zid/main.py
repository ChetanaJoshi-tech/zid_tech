# # app/main.py
# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from zid.database import engine, SessionLocal, Base
# from zid import crud, models

# # Create tables in the database
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/sales_products/")
# def create_sales_product( db: Session = Depends(get_db)):
#     return crud.create_sales_product(db=db)

# @app.get("/sales_products/")
# def read_sales_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud.get_sales_products(db=db, skip=skip, limit=limit)



# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal, engine
from faker import Faker
from .models import SalesProducts
import random
import datetime


# Create the tables in the database (run this once to create the schema)


# Create FastAPI app
app = FastAPI()

faker = Faker()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create a sales product
@app.post("/sales_products/", response_model=schemas.SalesProductRead)
def create_sales_product(
    sales_product: schemas.SalesProductCreate, db: Session = Depends(get_db)
):
    return crud.create_sales_product(db=db, sales_product=sales_product)

# Route to get a list of sales products
@app.get("/sales_products/", response_model=list[schemas.SalesProductRead])
def read_sales_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sales_products(db=db, skip=skip, limit=limit)

# Route to get a single sales product by ID
@app.get("/sales_products/{product_id}", response_model=schemas.SalesProductRead)
def read_sales_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_sales_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/sales_product/")
def get_total_sales_value(
    start_date: datetime.date, end_date: datetime.date, db: Session = Depends(get_db)
):
    total_sales = crud.get_totals_sales_values_by_date_range(db, start_date, end_date)
    
    if total_sales is None:
        raise HTTPException(status_code=404, detail="No sales found in the given date range")
    
    return {"total_sales_value": total_sales}


@app.get("/sale_product/")
def get_total_sales_count(
    start_date: datetime.date, end_date: datetime.date, db: Session = Depends(get_db)
):
    count_sales = crud.get_totals_sales_count_by_date_range(db, start_date, end_date)
    
    if count_sales is None:
        raise HTTPException(status_code=404, detail="No sales found in the given date range")
    
    return {"total_sales_count": count_sales}



@app.get("/sales_productss/")
def get_total_sales_and_count(
    start_date: datetime.date, end_date: datetime.date, db: Session = Depends(get_db)
):
    result = crud.get_total_sales_and_count_by_date_range(db, start_date, end_date)
     
    total_sales_value, total_count = result

    if total_sales_value is None and total_count is None:
        raise HTTPException(status_code=404, detail="No sales found in the given date range")
    
   
    return {"result": {"total_sales_value" :total_sales_value, "total_count":total_count}}



#  Generate dummy data for initial setup
@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    for _ in range(5):  # Create 5 dummy records
        fake_product = SalesProducts(
            product_name=faker.word(),
            product_sku=faker.bothify(text="SKU-#####"),
            total_sales_value=random.uniform(100, 1000),
            orders_count=random.randint(1, 100),
            created_at=datetime.datetime.utcnow() 
        )
        db.add(fake_product)
    db.commit()
    db.close()
