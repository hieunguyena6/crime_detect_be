"""empty message

Revision ID: 345283f2876c
Revises: a7a21237954d
Create Date: 2021-01-23 15:34:35.604889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '345283f2876c'
down_revision = 'a7a21237954d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('percent', sa.Integer(), nullable=False),
    sa.Column('crime_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('custom_id', sa.Integer(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['crime_id'], ['crimes.id'], ),
    sa.ForeignKeyConstraint(['custom_id'], ['customs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    # ### end Alembic commands ###
