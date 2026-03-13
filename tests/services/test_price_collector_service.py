import pytest
from unittest.mock import AsyncMock, patch

from src.services.price_collector_service import PriceCollectorService


@pytest.mark.asyncio
async def test_collect_saves_prices():
    market_data_client = AsyncMock()
    price_repository = AsyncMock()

    async def fake_get_index_price(ticker: str):
        prices = {
            "btc_usd": 71381.0,
            "eth_usd": 2111.0,
        }
        return prices[ticker]

    market_data_client.get_index_price.side_effect = fake_get_index_price

    service = PriceCollectorService(
        market_data_client=market_data_client,
        price_repository=price_repository,
    )

    with patch(
        "src.services.price_collector_service.time.time", return_value=1700000000
    ):
        await service.collect()

    assert market_data_client.get_index_price.await_count == 2

    price_repository.create.assert_awaited_once_with(
        [
            {
                "ticker": "btc_usd",
                "price": 71381.0,
                "timestamp": 1700000000,
            },
            {
                "ticker": "eth_usd",
                "price": 2111.0,
                "timestamp": 1700000000,
            },
        ]
    )


@pytest.mark.asyncio
async def test_collect_raises_when_client_fails():
    market_data_client = AsyncMock()
    price_repository = AsyncMock()

    market_data_client.get_index_price.side_effect = RuntimeError("deribit error")

    service = PriceCollectorService(
        market_data_client=market_data_client,
        price_repository=price_repository,
    )

    with pytest.raises(RuntimeError, match="deribit error"):
        await service.collect()

    price_repository.create.assert_not_awaited()
