"""empty message

Revision ID: 46a81c671c22
Revises: 
Create Date: 2019-08-15 11:43:02.352529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46a81c671c22'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('augustje',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('embed', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('augustje_subscriber',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bar_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('upstairs', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(length=70), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('election',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('open', sa.Integer(), nullable=True),
    sa.Column('votesperperson', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('input',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('input', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('muilgraaf_person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('club', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schacht',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schachten_opdracht',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('fullname', sa.String(length=70), nullable=False),
    sa.Column('roles', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('voter_key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('election_option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('election', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['election'], ['election.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fulfilled',
    sa.Column('schacht_id', sa.Integer(), nullable=True),
    sa.Column('opdracht_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['opdracht_id'], ['schachten_opdracht.id'], ),
    sa.ForeignKeyConstraint(['schacht_id'], ['schacht.id'], )
    )
    op.create_table('muilgraaf_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_1', sa.Integer(), nullable=False),
    sa.Column('person_2', sa.Integer(), nullable=False),
    sa.Column('event', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['person_1'], ['muilgraaf_person.id'], ),
    sa.ForeignKeyConstraint(['person_2'], ['muilgraaf_person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('poef_transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bar_transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('order', sa.String(), nullable=False),
    sa.Column('poeftransaction', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poeftransaction'], ['poef_transaction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('votes',
    sa.Column('voterkey', sa.Integer(), nullable=True),
    sa.Column('electionid', sa.Integer(), nullable=True),
    sa.Column('optionid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['electionid'], ['election.id'], ),
    sa.ForeignKeyConstraint(['optionid'], ['election_option.id'], ),
    sa.ForeignKeyConstraint(['voterkey'], ['voter_key.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.drop_table('bar_transaction')
    op.drop_table('poef_transaction')
    op.drop_table('muilgraaf_link')
    op.drop_table('fulfilled')
    op.drop_table('election_option')
    op.drop_table('voter_key')
    op.drop_table('user')
    op.drop_table('schachten_opdracht')
    op.drop_table('schacht')
    op.drop_table('muilgraaf_person')
    op.drop_table('input')
    op.drop_table('election')
    op.drop_table('bar_item')
    op.drop_table('augustje_subscriber')
    op.drop_table('augustje')
    # ### end Alembic commands ###
