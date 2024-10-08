"""Change embedding column to Stringg

Revision ID: 65dcf46ef826
Revises: 1df42693e97e
Create Date: 2024-08-16 19:18:03.417215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65dcf46ef826'
down_revision: Union[str, None] = '1df42693e97e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_chunks_id'), 'chunks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_chunks_id'), table_name='chunks')
    # ### end Alembic commands ###
