"""Initial migration.

Revision ID: 7e8f4380af51
Revises: 
Create Date: 2023-03-05 19:06:30.976588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e8f4380af51'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('region', sa.String(length=30), nullable=False),
    sa.Column('province', sa.String(length=30), nullable=False),
    sa.Column('district', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stations')
    # ### end Alembic commands ###
