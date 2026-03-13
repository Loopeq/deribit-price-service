from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(index=True, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    timestamp: Mapped[int] = mapped_column(index=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
