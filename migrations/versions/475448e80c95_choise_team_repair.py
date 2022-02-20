"""Choise team repair

Revision ID: 475448e80c95
Revises: cc0b9a8c6bec
Create Date: 2022-02-20 14:49:35.862420

"""
from alembic import op
import sqlalchemy as sa

from app.enums import ChoiceType
from app.choises import equipment, team_composition


# revision identifiers, used by Alembic.
revision = '475448e80c95'
down_revision = 'cc0b9a8c6bec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('log', sa.Column('team_composition', ChoiceType(team_composition), nullable=True))
    op.add_column('log', sa.Column('equipment_repair', ChoiceType(equipment), nullable=True))
    # op.drop_index('ix_log_pub_date', table_name='log')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_index('ix_log_pub_date', 'log', ['pub_date'], unique=False)
    op.drop_column('log', 'equipment_repair')
    op.drop_column('log', 'team_composition')
    # ### end Alembic commands ###
