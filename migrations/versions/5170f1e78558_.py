"""empty message

Revision ID: 5170f1e78558
Revises: cbf91883bb6a
Create Date: 2021-01-11 11:51:55.514671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5170f1e78558'
down_revision = 'cbf91883bb6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crimes', sa.Column('face_image', sa.String(length=1500000), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('crimes', 'face_image')
    # ### end Alembic commands ###
