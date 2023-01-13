"""deleted notes

Revision ID: dc52390ea8e0
Revises: 13838c5d2532
Create Date: 2023-01-12 21:30:55.994370

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dc52390ea8e0'
down_revision = '13838c5d2532'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('detail', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('is_public', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('is_archived', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='notes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='notes_pkey')
    )
    # ### end Alembic commands ###