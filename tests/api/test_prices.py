import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.api.dependencies import get_db
from src.repositories.price_repository import PriceRepository


class FakePrice:
    def __init__(self, id: int, ticker: str, price: float, timestamp: int) -> None:
        self.id = id
        self.ticker = ticker
        self.price = price
        self.timestamp = timestamp


class FakeSession:
    pass


async def override_get_db():
    yield FakeSession()


@pytest.fixture(autouse=True)
def setup_dependency_override():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_prices(monkeypatch):
    async def fake_get(self, ticker: str):
        return [
            FakePrice(id=1, ticker=ticker, price=71381.0, timestamp=1700000000),
            FakePrice(id=2, ticker=ticker, price=72000.0, timestamp=1700000060),
        ]

    monkeypatch.setattr(PriceRepository, "get", fake_get)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/v1/price/", params={"ticker": "btc_usd"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "ticker": "btc_usd",
            "price": 71381.0,
            "timestamp": 1700000000,
        },
        {
            "id": 2,
            "ticker": "btc_usd",
            "price": 72000.0,
            "timestamp": 1700000060,
        },
    ]


@pytest.mark.asyncio
async def test_get_latest_price(monkeypatch):
    async def fake_get_latest(self, ticker: str):
        return FakePrice(id=10, ticker=ticker, price=65200.0, timestamp=1700000120)

    monkeypatch.setattr(PriceRepository, "get_latest", fake_get_latest)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/v1/price/latest", params={"ticker": "btc_usd"})

    assert response.status_code == 200
    assert response.json() == {
        "id": 10,
        "ticker": "btc_usd",
        "price": 65200.0,
        "timestamp": 1700000120,
    }


@pytest.mark.asyncio
async def test_get_prices_in_range(monkeypatch):
    async def fake_get_by(self, ticker: str, from_ts: int, to_ts: int):
        return [
            FakePrice(id=3, ticker=ticker, price=64950.0, timestamp=1700000000),
            FakePrice(id=4, ticker=ticker, price=65050.0, timestamp=1700000060),
        ]

    monkeypatch.setattr(PriceRepository, "get_by", fake_get_by)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/v1/price/range",
            params={
                "ticker": "btc_usd",
                "from_ts": 1700000000,
                "to_ts": 1700000100,
            },
        )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 3,
            "ticker": "btc_usd",
            "price": 64950.0,
            "timestamp": 1700000000,
        },
        {
            "id": 4,
            "ticker": "btc_usd",
            "price": 65050.0,
            "timestamp": 1700000060,
        },
    ]


@pytest.mark.asyncio
async def test_ticker_is_required():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/v1/price/latest")

    assert response.status_code == 422
