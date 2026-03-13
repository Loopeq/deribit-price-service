from src.db.session import db_session
from src.client.market_data import MarketDataClient
from src.repositories.price_repository import PriceRepository
from src.services.price_collector_service import PriceCollectorService
from src.core.celery_app import celery_app
import aiohttp
import asyncio


async def collect_prices_impl() -> None:
    async with aiohttp.ClientSession() as http_session:
        async with db_session() as session:
            repository = PriceRepository(session=session)
            client = MarketDataClient(session=http_session)

            collector = PriceCollectorService(
                market_data_client=client,
                price_repository=repository,
            )
            await collector.collect()


@celery_app.task(name="collect_prices", max_retries=3)
def collect_prices():
    asyncio.run(collect_prices_impl())
