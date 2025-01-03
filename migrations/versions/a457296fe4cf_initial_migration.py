"""Initial migration

Revision ID: a457296fe4cf
Revises: 
Create Date: 2024-07-29 18:34:19.795171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a457296fe4cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('discovered_magazines', sa.Integer(), nullable=True),
    sa.Column('assigned_magazines', sa.PickleType(), nullable=True),
    sa.Column('magazine_list', sa.String(length=1), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('route', sa.String(length=1), nullable=False),
    sa.Column('meeting_place', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('family_task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword', sa.String(length=50), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patrol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=False),
    sa.Column('time_penalty', sa.Integer(), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('used_keyword',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword', sa.String(length=50), nullable=False),
    sa.Column('patrol_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['patrol_id'], ['patrol.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('used_keyword')
    op.drop_table('patrol')
    op.drop_table('family_task')
    op.drop_table('family')
    # ### end Alembic commands ###
