from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/price")
async def price(ticker: str):
    return ticker


@router.get("/price/range")
async def price_range(ticker: str, from_ts: int, to_ts: int):
    return ticker, from_ts, to_ts


@router.get("/price/latest")
async def price_latest(ticker: str):
    return f"latest {ticker}"
