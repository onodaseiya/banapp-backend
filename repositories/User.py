from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    coin: int = 30
    cigarette_price: int
    cigarette_per_day: int


class CoinUpdate(BaseModel):
    coin: int
