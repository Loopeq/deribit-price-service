from fastapi import APIRouter
from src.client.market_data import MarketDataClient
import aiohttp
import asyncio

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/price")
async def price(ticker: str):
    async with aiohttp.ClientSession() as session:
        client = MarketDataClient(session)

        btc_usd, eth_usd = await asyncio.gather(
            client.get_index_price("btc_usd"), client.get_index_price("eth_usd")
        )

    return btc_usd, eth_usd


@router.get("/price/range")
async def price_range(ticker: str, from_ts: int, to_ts: int):
    return ticker, from_ts, to_ts


@router.get("/price/latest")
async def price_latest(ticker: str):
    return f"latest {ticker}"
