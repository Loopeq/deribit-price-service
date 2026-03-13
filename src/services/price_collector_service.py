import time

from src.core.constants import TICKERS
from src.client.market_data import MarketDataClient
from src.repositories.price_repository import PriceRepository
import asyncio


class PriceCollectorService:
    def __init__(
        self,
        market_data_client: MarketDataClient,
        price_repository: PriceRepository,
    ) -> None:
        self.market_data_client = market_data_client
        self.price_repository = price_repository

    async def collect(self) -> None:
        tickers = list(TICKERS)
        timestamp = int(time.time())

        prices = await asyncio.gather(
            *(self.market_data_client.get_index_price(ticker) for ticker in tickers)
        )

        rows = [
            {"ticker": ticker, "price": price, "timestamp": timestamp}
            for ticker, price in zip(tickers, prices)
        ]

        await self.price_repository.create(rows)
