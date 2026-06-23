from enum import Enum

import sqlalchemy as sa

from dio_bank.database import metadata


class TransactionType(str, Enum):
    deposit = 'deposit'
    withdraw = 'withdraw'


transactions = sa.Table(
    'transactions',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column(
        'account_id',
        sa.Integer,
        sa.ForeignKey('accounts.id', ondelete='CASCADE'),
        nullable=False,
    ),
    sa.Column('transaction', sa.Enum(TransactionType), nullable=False),
    sa.Column('amount', sa.Float, nullable=False),
    sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), default=sa.func.now()
    ),
)
