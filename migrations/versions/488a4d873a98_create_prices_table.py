"""create prices table

Revision ID: 488a4d873a98
Revises: 
Create Date: 2026-03-13 20:04:19.968975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '488a4d873a98'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('prices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ticker', sa.String(length=20), nullable=False),
    sa.Column('price', sa.Numeric(precision=18, scale=8), nullable=False),
    sa.Column('timestamp', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prices_ticker'), 'prices', ['ticker'], unique=False)
    op.create_index(op.f('ix_prices_timestamp'), 'prices', ['timestamp'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_prices_timestamp'), table_name='prices')
    op.drop_index(op.f('ix_prices_ticker'), table_name='prices')
    op.drop_table('prices')
