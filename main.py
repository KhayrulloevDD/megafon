import os
import time

import requests
from typing import List

from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

import models
import schemas
import dbs.databases as databases


app = FastAPI()


@app.get("/payments_pg", response_model=List[schemas.Payment])
async def get_payments_pg(limit: int = 10, pg_db: Session = Depends(databases.get_pg_db)):
    try:
        return pg_db.query(models.PGPayment).limit(limit).all()
    except Exception as e:
        return {
            "message": f"An error has occurred: {e}",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
        }

@app.post("/payments_pg", response_model=schemas.Payment)
async def create_payment_pg(payment: schemas.PaymentIn, pg_db: Session = Depends(databases.get_pg_db)):
    try:
        new_payment = models.PGPayment(phone=payment.phone, amount=payment.amount, description=payment.description)
        pg_db.add(new_payment)
        pg_db.commit()
        pg_db.refresh(new_payment)
        return new_payment
    except Exception as e:
        return {
            "message": f"An error has occurred: {e}",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
        }


@app.get("/payments", response_model=List[schemas.Payment])
async def get_payments(limit: int = 10, db: Session = Depends(databases.get_db)):
    try:
        return db.query(models.Payment).limit(limit).all()
    except Exception as e:
        return {
            "message": f"An error has occurred: {e}",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
        }


@app.post("/payments", response_model=schemas.Payment)
async def create_payment(payment: schemas.PaymentIn, db: Session = Depends(databases.get_db)):
    try:
        new_payment = models.Payment(phone=payment.phone, amount=payment.amount, description=payment.description)
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except Exception as e:
        return {
            "message": f"An error has occurred: {e}",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
        }


@app.get("/service1", status_code=status.HTTP_200_OK)
async def agify(name: str = 'bella'):
    url = f'https://api.agify.io/?name={name}'
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "message": f"Connection error at '{url}': {e}",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
        }


@app.get("/service2/{venue_id}", status_code=status.HTTP_200_OK)
async def coin_map(venue_id: int):
    url = f'https://coinmap.org/api/v1/venues/{venue_id}'
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "message": f"Connection error at '{url}': {e}",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
        }


# uvicorn main:app --reload
