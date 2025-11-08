from pydantic import BaseModel, Field


class CartProduct(BaseModel):
    quantity: int
    id: str


class PaymentRequest(BaseModel):
    currency: str = "mxn"
    listProducts: list[CartProduct]