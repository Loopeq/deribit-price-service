from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.price import PriceResponse
from src.repositories.price_repository import PriceRepository
from src.api.dependencies import get_db

router = APIRouter(prefix="/price", tags=["Market"])


@router.get("/", response_model=list[PriceResponse])
async def price(ticker: str, db: AsyncSession = Depends(get_db)):
    repo = PriceRepository(db)
    return await repo.get(ticker=ticker)


@router.get("/range", response_model=list[PriceResponse])
async def price_range(
    ticker: str, from_ts: int, to_ts: int, db: AsyncSession = Depends(get_db)
):
    repo = PriceRepository(db)
    return await repo.get_by(ticker=ticker, from_ts=from_ts, to_ts=to_ts)


@router.get("/latest", response_model=PriceResponse)
async def price_latest(ticker: str, db: AsyncSession = Depends(get_db)):
    repo = PriceRepository(db)
    return await repo.get_latest(ticker=ticker)
