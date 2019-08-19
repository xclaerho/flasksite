"""empty message

Revision ID: 6935a483f037
Revises: 46a81c671c22
Create Date: 2019-08-15 17:57:26.791130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6935a483f037'
down_revision = '46a81c671c22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bar_item', 'upstairs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bar_item', sa.Column('upstairs', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
