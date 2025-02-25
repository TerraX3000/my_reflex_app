"""empty message

Revision ID: f1794cb49d3c
Revises: 75c436cedef8
Create Date: 2025-02-06 22:43:43.821832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'f1794cb49d3c'
down_revision: Union[str, None] = '75c436cedef8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_format', sqlmodel.sql.sqltypes.AutoString(), server_default=sa.text("'%Y-%m-%d'"), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_column('date_format')

    # ### end Alembic commands ###
