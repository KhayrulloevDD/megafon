import os

import requests
from typing import List

from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

import models
import schemas
from services import call_apis
from dbs.databases import get_db, get_pg_db


app = FastAPI()


@app.get("/payments_pg/", response_model=List[schemas.Payment])
async def get_payments_pg(limit: int = 10, pg_db: Session = Depends(get_pg_db)):
    return pg_db.query(models.PGPayment).limit(limit).all()


@app.post("/payments_pg/", response_model=schemas.Payment)
async def create_payment_pg(payment: schemas.PaymentIn, pg_db: Session = Depends(get_pg_db)):
    new_payment = models.PGPayment(phone=payment.phone, amount=payment.amount, description=payment.description)
    pg_db.add(new_payment)
    pg_db.commit()
    pg_db.refresh(new_payment)
    return new_payment


@app.get("/payments/", response_model=List[schemas.Payment])
async def get_payments(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Payment).limit(limit).all()


@app.post("/payments/", response_model=schemas.Payment)
async def create_payment(payment: schemas.PaymentIn, db: Session = Depends(get_db)):
    new_payment = models.Payment(phone=payment.phone, amount=payment.amount, description=payment.description)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@app.get("/service1", status_code=status.HTTP_200_OK)
async def agify(name: str = 'bella'):
    url = f'https://api.agify.io/?name={name}'
    response = requests.get(url)
    return response.json()


@app.get("/service2/{venue_id}", status_code=status.HTTP_200_OK)
async def coin_map(venue_id: int):
    url = f'https://coinmap.org/api/v1/venues/{venue_id}'
    response = requests.get(url)
    return response.json()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return await call_apis()

# uvicorn main:app --reload
