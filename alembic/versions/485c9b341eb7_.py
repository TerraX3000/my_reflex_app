"""empty message

Revision ID: 485c9b341eb7
Revises: e16c63b7eceb
Create Date: 2025-02-19 19:17:22.340817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '485c9b341eb7'
down_revision: Union[str, None] = 'e16c63b7eceb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_expense_category', sa.Boolean(), server_default=sa.text('1'), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_column('is_expense_category')

    # ### end Alembic commands ###
