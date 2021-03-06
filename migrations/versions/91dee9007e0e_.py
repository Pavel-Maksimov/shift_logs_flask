"""empty message

Revision ID: 91dee9007e0e
Revises: 89b1b122e518
Create Date: 2022-02-20 13:09:17.976020

"""
from alembic import op
import sqlalchemy as sa

from app.enums import ValueEnum


# revision identifiers, used by Alembic.
revision = '91dee9007e0e'
down_revision = '89b1b122e518'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('log', sa.Column('shift_time', ValueEnum('00:00-08:00', '08:00-16:00', '16:00-00:00', name='shifttime'), nullable=True))
    op.alter_column('log', sa.Column('team', ValueEnum('А', 'Б', 'В', 'Г', 'Д', name='team'), nullable=True))
    # op.drop_index('ix_log_pub_date', table_name='log')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_index('ix_log_pub_date', 'log', ['pub_date'], unique=False)
    op.alter_column('log', sa.Column('shift_time', sa.Enum('00:00-08:00', '08:00-16:00', '16:00-00:00', name='shifttime'), nullable=True))
    op.alter_column('log', sa.Column('team', sa.Enum('А', 'Б', 'В', 'Г', 'Д', name='team'), nullable=True))
    # ### end Alembic commands ###
