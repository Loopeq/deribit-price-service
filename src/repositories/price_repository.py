from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.price import Price


class PriceRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, ticker: str, price: float, timestamp: int) -> Price:
        payload = Price(
            ticker=ticker,
            price=price,
            timestamp=timestamp,
        )
        self.session.add(payload)
        await self.session.commit()
        await self.session.refresh(payload)
        return payload

    async def get(self, ticker: str) -> list[Price]:
        query = (
            select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.asc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_latest(self, ticker: str) -> Price | None:
        query = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(desc(Price.timestamp))
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by(
        self,
        ticker: str,
        from_ts: int,
        to_ts: int,
    ) -> list[Price]:
        query = (
            select(Price)
            .where(
                Price.ticker == ticker,
                Price.timestamp >= from_ts,
                Price.timestamp <= to_ts,
            )
            .order_by(Price.timestamp.asc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
