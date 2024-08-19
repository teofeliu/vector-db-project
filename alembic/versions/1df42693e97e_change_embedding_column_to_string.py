"""Change embedding column to String

Revision ID: 1df42693e97e
Revises: 4f45c2954515
Create Date: 2024-08-16 18:59:07.400029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1df42693e97e'
down_revision = '4f45c2954515'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the desired schema
    op.create_table('chunks_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('embedding', sa.String(), nullable=True),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copy data from the old table to the new table
    op.execute('INSERT INTO chunks_new SELECT id, content, json(embedding), document_id FROM chunks')
    
    # Drop the old table
    op.drop_table('chunks')
    
    # Rename the new table to the original table name
    op.rename_table('chunks_new', 'chunks')

def downgrade():
    # Create a new table with the old schema
    op.create_table('chunks_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('embedding', sa.JSON(), nullable=True),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copy data from the current table to the old schema table
    op.execute('INSERT INTO chunks_old SELECT id, content, json(embedding), document_id FROM chunks')
    
    # Drop the current table
    op.drop_table('chunks')
    
    # Rename the old schema table to the original table name
    op.rename_table('chunks_old', 'chunks')