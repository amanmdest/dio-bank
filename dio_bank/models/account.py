import sqlalchemy as sa

from dio_bank.database import metadata

accounts = sa.Table(
    'accounts',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('holder', sa.String(150), nullable=False, unique=True),
    sa.Column('balance', sa.Float, default=0.0),
    sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), default=sa.func.now()
    ),
)
