from pydantic import BaseModel, ConfigDict


class PriceCreate(BaseModel):
    ticker: str
    price: float
    timestamp: int


class PriceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticker: str
    price: float
    timestamp: int
