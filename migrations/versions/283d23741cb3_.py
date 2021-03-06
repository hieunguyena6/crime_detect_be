"""empty message

Revision ID: 283d23741cb3
Revises: 809445e41b69
Create Date: 2021-04-14 10:09:18.469465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '283d23741cb3'
down_revision = '809445e41b69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###
