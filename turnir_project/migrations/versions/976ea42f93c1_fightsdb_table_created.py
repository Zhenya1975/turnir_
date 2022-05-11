"""fightsdb table created

Revision ID: 976ea42f93c1
Revises: 
Create Date: 2022-05-11 15:01:25.302715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '976ea42f93c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fightsDB',
    sa.Column('fight_id', sa.Integer(), nullable=False),
    sa.Column('round_number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('fight_id')
    )
    op.create_table('participantsDB',
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('participant_first_name', sa.String(), nullable=True),
    sa.Column('participant_last_name', sa.String(), nullable=True),
    sa.Column('activity_status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('participant_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('participantsDB')
    op.drop_table('fightsDB')
    # ### end Alembic commands ###