"""empty message

Revision ID: 07b66faedc30
Revises: 6ebf809894c2
Create Date: 2020-12-27 00:28:24.424707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07b66faedc30'
down_revision = '6ebf809894c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=128),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=sa.String(length=128),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###