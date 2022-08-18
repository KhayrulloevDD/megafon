from pydantic import BaseModel


class PaymentIn(BaseModel):
    phone: str
    amount: int
    description: str

    class Config:
        orm_mode = True


class Payment(PaymentIn):
    id: int

    class Config:
        orm_mode = True
