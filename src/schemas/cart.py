from pydantic import BaseModel, ConfigDict


class CartItemAdd(BaseModel):
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int = 1


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    quantity: int
    product_name: str
    price: int


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[CartItemResponse] = []
    total_price: int
